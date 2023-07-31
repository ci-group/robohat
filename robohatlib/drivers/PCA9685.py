# !/usr/bin/env python



import math

try:
    from robohatlib.helpers.RoboUtil import RoboUtil
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
    from robohatlib.Robohat_config import DEBUG
except ImportError:
    print("Failed to import RoboUtil")
    raise


# Define registers values from the datasheet
MODE1_ADDRESS =         0x00
MODE2_ADDRESS =         0x01
SUBADR1_ADDRESS =       0x02
SUBADR2_ADDRESS =       0x03
SUBADR3_ADDRESS =       0x04
ALLCALLADR_ADDRESS =    0x05
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
MODE1_EXTCLK_BITNR =    6  # use external clock
MODE1_SLEEP_BITNR =     4  # sleep mode
MODE1_ALLCALL_BITNR =   0  # all call address

MODE2_INVRT_BITNR =     4  # invert output
MODE2_OCH_BITNR =       3  # output type
MODE2_OUTDRV_BITNR =    2  # output type
MODE2_OUTNE1_BITNR =    0  # output mode when not enabled



"""!
~OE ie via een jumper       input pca
INT_i2C gpio4               output pca, input cpu
bus i2c-1
"""

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
    def init_pca9685(self) -> None:
        """!
        Initializes PCA9685
        @return None:
        """
        if DEBUG is True:
            print("init_pca9685")

        self.__do_idle()
        self.__do_invert_and_set_driver_to_pushpull()
        self.wake()
        self.__set_pwm_freq(50)






    # --------------------------------------------------------------------------------------
    def set_on_time_channel(self, _channel: int, _time_wanted_us: float) -> None:
        """!
        @param _channel: channel nr 0 - 15
        @param _time_wanted_us: new time in uS
        @return: None
        """
        if _channel >= 0 and _channel < 16:
            actual_ticks_on = self.__convert_timeUs_to_tick(_time_wanted_us)

            on_ticks = 0
            off_ticks = 4095 - actual_ticks_on - on_ticks

            on_tick_bytes = on_ticks.to_bytes(2, 'little')
            off_tick_bytes = off_ticks.to_bytes(2, 'little')

            self.__i2c_device.i2c_write_bytes(bytes([LED0_ON_L_ADDRESS + (4 * _channel), on_tick_bytes[0], on_tick_bytes[1], off_tick_bytes[0], off_tick_bytes[1]]))
        else:
            print("Error: channel " + str(_channel) + " in ADC MAX11607 not available")
    # --------------------------------------------------------------------------------------
    def set_on_time_all_channels(self, _wanted_times_us: []) -> None:
        """!

        @param _wanted_times_us:
        @return: None
        """
        data_to_send = bytes([LED0_ON_L_ADDRESS])
        for i in range(0, 16):
            actual_ticks_on = self.__convert_timeUs_to_tick(_wanted_times_us[i])
            on_ticks = 0
            off_ticks = 4095 - actual_ticks_on - on_ticks

            on_tick_bytes = on_ticks.to_bytes(2, 'little')
            off_tick_bytes = off_ticks.to_bytes(2, 'little')

            data_to_send = data_to_send + bytes([on_tick_bytes[0], on_tick_bytes[1], off_tick_bytes[0], off_tick_bytes[1]])
            self.__i2c_device.i2c_write_bytes(data_to_send)

    # --------------------------------------------------------------------------------------
    def sleep(self) -> None:
        """!
        Put the device into a sleep state
        @return: None
        """
        old_mode = self.__read(MODE1_ADDRESS)
        new_mode = old_mode | (1 << MODE1_SLEEP_BITNR)
        self.__write(MODE1_ADDRESS, new_mode)
        self.__i_am_a_sleep = True
    # --------------------------------------------------------------------------------------
    def wake(self) -> None:
        """!
        Wake the device from its sleep state
        @return: None
        """
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
        return self.__i_am_a_sleep

    #--------------------------------------------------------------------------------------
    def __set_pwm_freq(self, _freq: int, _calibration: int=-3) -> None:
        """!
        Set the PWM frequency
        @param _freq: 40 to 1000
        @type _freq: int
        @param _calibration: optional integer value to offset oscillator errors. defaults to 0
        @raises ValueError: set_pwm_freq: freq out of range
        """
        if _freq < 40 or _freq > 1000:
            raise ValueError('set_pwm_freq: freq out of range')

        scale_val = 25000000.0               # 25MHz
        scale_val = scale_val / 4096.0        # 12-bit
        scale_val = scale_val / float(_freq)
        scale_val = scale_val - 1
        pre_scale = math.floor(scale_val + 0.5)
        pre_scale = pre_scale + float(_calibration)

        self.__freq = _freq

        self.sleep()
        self.__write(PRE_SCALE_ADDRESS, int(pre_scale))
        self.wake()

    # --------------------------------------------------------------------------------------

    def __convert_timeUs_to_tick(self, _time_wanted_us: float) -> int:
        time_per_tick = ((1.0 / self.__freq) / 4095.0) * 1000000
        actual_ticks = int(_time_wanted_us / time_per_tick)
        return actual_ticks

    def __do_invert_and_set_driver_to_pushpull(self):
        old_mode = self.__read(MODE2_ADDRESS)
        new_mode = old_mode | (1 << MODE2_INVRT_BITNR)
        new_mode = new_mode | (1 << MODE2_OUTDRV_BITNR)
        self.__write(MODE2_ADDRESS, new_mode)

    # --------------------------------------------------------------------------------------
    def __do_idle(self) -> None:
        self.__write(0x00, 0x00)

    # --------------------------------------------------------------------------------------
    def __write(self, reg, value) -> None:
        self.__i2c_device.i2c_write_register_byte(reg, value)
        #self.__i2c_device.i2c_write_bytes(bytes([reg, value]))

    # --------------------------------------------------------------------------------------
    def __read(self, reg):
        """!

        @param reg:
        @return:
        """

        return_value_array = bytearray(2)
        self.__i2c_device.write_to_then_read_from(bytes([0x00, reg]), return_value_array)

        return return_value_array[0]

    # --------------------------------------------------------------------------------------



