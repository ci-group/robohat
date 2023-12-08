"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Driver of PCA9685.
PCA9685 is a 12 bit, 16 channel PWM driver controlled by I2C

Needed is the connected I2C-bus
@init _should_be_time can be given. When absent he time will be the default time
"""

try:
    import math
    from robohatlib.helpers.RoboUtil import RoboUtil
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
    from robohatlib.RobohatConfig import DEBUG
    from robohatlib.RobohatConfig import SERVO_DEFAULT_PWM_FREQ
    from time import sleep
except ImportError:
    print("Failed to resolve dependencies for the PCA9685")
    raise


# Define registers values from the datasheet
MODE1_ADDRESS =         0x00
MODE2_ADDRESS =         0x01
SUB_ADR1_ADDRESS =      0x02
SUB_ADR2_ADDRESS =      0x03
SUB_ADR3_ADDRESS =      0x04
ALL_CALL_ADR_ADDRESS =  0x05
LED0_ON_L_ADDRESS =     0x06
LED0_ON_H_ADDRESS =     0x07
LED0_OFF_L_ADDRESS =    0x08
LED0_OFF_H_ADDRESS =    0x09
ALL_LED_ON_L_ADDRESS =  0xFA
ALL_LED_ON_H_ADDRESS =  0xFB
ALL_LED_OFF_L_ADDRESS = 0xFC
ALL_LED_OFF_H_ADDRESS = 0xFD
PRE_SCALE_ADDRESS =     0xFE

# Define mode bits
MODE_1_RESTART_BITNR =  7  # restart bit
MODE1_EXT_CLK_BITNR =   6  # use external clock
MODE1_SLEEP_BITNR =     4  # sleep mode
MODE1_ALL_CALL_BITNR =  0  # all call address

MODE2_INVRT_BITNR =     4  # invert output
MODE2_OCH_BITNR =       3  # output type
MODE2_OUTDRV_BITNR =    2  # output type
MODE2_OUTNE1_BITNR =    0  # output mode when not enabled


class PCA9685:

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __init__(self, _i2c_device: I2CDevice):
        """!
        Constructor
        @param _i2c_device: connection IO
        """

        self.__i2c_device = _i2c_device
        self.__i_am_a_sleep = False

    # --------------------------------------------------------------------------------------

    def init_pca9685(self, _should_be_time = None) -> None:
        """!
        Initializes PCA9685 and set time of the current angles
        @return None:
        """

        self.__do_idle()
        self.__do_invert_and_set_driver_to_pushpull()

        self.__set_pwm_freq(SERVO_DEFAULT_PWM_FREQ)

        self.put_to_sleep()

        if _should_be_time is not None:
            self.set_on_time_all_channels(_should_be_time, False)

        self.wake_up()
    # --------------------------------------------------------------------------------------
    def set_on_time_channel(self, _channel: int, _time_wanted_us: float) -> None:
        """!
        @param _channel: channel nr 0 - 15
        @param _time_wanted_us: new time in uS
        @return: None
        """

        if self.is_sleeping() is True:
            print("Can't set new servo value. Servos are sleeping")
        else:
            if _channel >= 0 and _channel < 16:
                actual_ticks_on = self.__convert_time_us_to_tick(_time_wanted_us)

                if DEBUG is True:
                    time_per_hz = (1000000 / self.__freq) / 4096.0
                    time_us = actual_ticks_on * time_per_hz
                    print("on reg val: " + str(actual_ticks_on) + " time: " + str(int(time_us)) + " uS")

                on_ticks = 0                                            # default offset value
                off_ticks = 4095 - actual_ticks_on - on_ticks

                on_tick_bytes = on_ticks.to_bytes(2, 'little')
                off_tick_bytes = off_ticks.to_bytes(2, 'little')

                self.__i2c_device.i2c_write_bytes(bytes([LED0_ON_L_ADDRESS + (4 * _channel), on_tick_bytes[0], on_tick_bytes[1], off_tick_bytes[0], off_tick_bytes[1]]))

                if DEBUG is True:
                    print("set_on_time_channel: " + str(_channel) + " " + str(on_ticks))

            else:
                print("Error: channel " + str(_channel) + " in PWM PCA9685 not available")
    # --------------------------------------------------------------------------------------
    def set_on_time_all_channels(self, _wanted_times_us: [], _warn_if_sleeping: bool = True) -> None:
        """!
        @param _warn_if_sleeping: warns if set to true, if servos are sleeping
        @param _wanted_times_us: a list of 16, with the times
        @return: None
        """

        if self.is_sleeping() and _warn_if_sleeping is True:
            print("Can't set new servo value. Servos are sleeping")
        else:
            if _wanted_times_us is not None:
                data_to_send = bytes([LED0_ON_L_ADDRESS])
                for i in range(0, 16):

                    wanted_time = _wanted_times_us[i]
                    actual_ticks_on = self.__convert_time_us_to_tick(wanted_time)

                    if DEBUG is True:
                        time_per_hz = (1000000 / self.__freq) / 4096.0
                        time_us = actual_ticks_on * time_per_hz
                        print(str(i) + ": on reg val: " + str(actual_ticks_on) + " time: " + str(int(time_us)) + " uS")

                    on_ticks = 0                                    # default offset value
                    off_ticks = 4095 - actual_ticks_on - on_ticks

                    on_tick_bytes = on_ticks.to_bytes(2, 'little')
                    off_tick_bytes = off_ticks.to_bytes(2, 'little')

                    data_to_send = data_to_send + bytes([on_tick_bytes[0], on_tick_bytes[1], off_tick_bytes[0], off_tick_bytes[1]])
                    self.__i2c_device.i2c_write_bytes(data_to_send)

    # --------------------------------------------------------------------------------------
    def put_to_sleep(self) -> None:
        """!
        Put the device into a sleep state
        @return: None
        """

        self.__i_am_a_sleep = True      # other thread is locked

        old_mode = self.__read(MODE1_ADDRESS)
        new_mode = (old_mode & 0x7F) | 0x10   # old_mode | (1 << MODE1_SLEEP_BITNR)
        self.__write(MODE1_ADDRESS, new_mode)

        if DEBUG is True:
            print("Sleep im PCA9685")

    # --------------------------------------------------------------------------------------
    def wake_up(self) -> None:
        """!
        Wake the device from its sleep state
        @return: None
        """
        self.__do_invert_and_set_driver_to_pushpull()

        self.__write(MODE1_ADDRESS, 0x0000)
        new_mode = 0x00a0
        self.__write(MODE1_ADDRESS, new_mode)
        self.__i_am_a_sleep = False

    # --------------------------------------------------------------------------------------
    def is_sleeping(self) -> bool:
        """!
        Check the sleep status of the device
        @return: True or False
        """
        # reg_val = self.__read(MODE1_ADDRESS)
        # if RoboUtil.check_bit(reg_val, MODE1_SLEEP_BITNR):
        #     return True
        # else:
        #     return False
        #
        #
        return self.__i_am_a_sleep

    #--------------------------------------------------------------------------------------
    def __set_pwm_freq(self, _freq: int) -> None:
        """!
        Set the PWM frequency
        @param _freq: 40 to 1000
        @type _freq: int
        @raises ValueError: set_pwm_freq: freq out of range
        """
        if _freq < 40 or _freq > 1000:
            print('set_pwm_freq: freq out of range')
        else:
            scale_val = 25000000.0               # 25MHz
            scale_val = scale_val / 4096.0        # 12-bit
            scale_val = scale_val / float(_freq)
            scale_val = scale_val - 1
            pre_scale = math.floor(scale_val + 0.5)

            self.__freq = _freq

            self.put_to_sleep()
            self.__write(PRE_SCALE_ADDRESS, int(pre_scale))
            self.wake_up()

    # --------------------------------------------------------------------------------------

    def __convert_time_us_to_tick(self, _time_wanted_us: float) -> int:
        """!
        Convert time in uS to tick needed for the register of the PCA9685
        @param _time_wanted_us:  time in uS
        @return: ticks
        """
        time_per_tick = ((1.0 / self.__freq) / 4095.0) * 1000000
        actual_ticks = int(_time_wanted_us / time_per_tick)
        return actual_ticks

    # --------------------------------------------------------------------------------------

    def __do_normal_and_set_driver_to_pullup(self) -> None:
        """!
        Set the driver to pushpull mode, and invert the outputs
        @return None
        """

        old_mode = self.__read(MODE2_ADDRESS)
        new_mode = old_mode & ~(1 << MODE2_INVRT_BITNR)
        new_mode = new_mode & ~(1 << MODE2_OUTDRV_BITNR)
        self.__write(MODE2_ADDRESS, new_mode)

    # --------------------------------------------------------------------------------------
    def __do_invert_and_set_driver_to_pushpull(self) -> None:
        """!
        Set the driver to pushpull mode, and invert the outputs
        @return None
        """

        old_mode = self.__read(MODE2_ADDRESS)
        new_mode = old_mode | (1 << MODE2_INVRT_BITNR)
        new_mode = new_mode | (1 << MODE2_OUTDRV_BITNR)
        self.__write(MODE2_ADDRESS, new_mode)

    # --------------------------------------------------------------------------------------
    def __do_idle(self) -> None:
        """!
         @return None
        """
        self.__write(MODE1_ADDRESS, 0x00)

    # --------------------------------------------------------------------------------------
    def __write(self, reg, value) -> None:
        """!
        @param reg: wanted register
        @param value:  value to put into register
        @return: None
        """
        self.__i2c_device.i2c_write_register_byte(reg, value)

    # --------------------------------------------------------------------------------------
    def __read(self, reg):
        """!
        @param reg: wanted register
        @return: register value
        """

        return_value_array = bytearray(2)
        self.__i2c_device.write_to_then_read_from(bytes([0x00, reg]), return_value_array)

        return return_value_array[0]

    # --------------------------------------------------------------------------------------


