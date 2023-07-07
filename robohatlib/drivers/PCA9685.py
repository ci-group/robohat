# !/usr/bin/env python


'''
~OE ie via een jumper       input pca
INT_i2C gpio4               output pca, input cpu
bus i2c-1

'''

import math

try:
    from robohatlib.helpers.RoboUtil import RoboUtil
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

class PCA9685:

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __init__(self, _i2cdevice):
        self.__i2cdevice = _i2cdevice

    # --------------------------------------------------------------------------------------
    def init_pca9685(self):
        print("init pca9685")

        print("--------------------------------------")
        self.__do_idle()
        self.__do_invert_and_setDriverToPushPull()
        self.__do_idle()
        self.__set_pwm_freq(50)

    # --------------------------------------------------------------------------------------
    def set_on_time_channel(self, _channel, _time_wanted_us):
        _channel = _channel - 1

        actual_ticks_on = self.__convert_timeUs_to_tick(_time_wanted_us)

        on_ticks = 0
        off_ticks = 4095 - actual_ticks_on - on_ticks

        #print("actual_ticks_on: " + str(actual_ticks_on) + ", on_ticks: " + str(on_ticks) + ", off_ticks: " + str(off_ticks))

        on_tick_bytes = on_ticks.to_bytes(2, 'little')
        off_tick_bytes = off_ticks.to_bytes(2, 'little')

        self.__i2cdevice.i2c_write_bytes(bytes([LED0_ON_L_ADDRESS + (4 * _channel), on_tick_bytes[0], on_tick_bytes[1], off_tick_bytes[0], off_tick_bytes[1]]))

    # --------------------------------------------------------------------------------------
    def set_on_time_allchannels(self, _wantedtimes_us):

        datatosend = bytes([LED0_ON_L_ADDRESS])

        for i in range(0, 16):
            actual_ticks_on = self.__convert_timeUs_to_tick(_wantedtimes_us[i])
            on_ticks = 0
            off_ticks = 4095 - actual_ticks_on - on_ticks

            #print("actual_ticks_on: " + str(actual_ticks_on) + ", on_ticks: " + str(on_ticks) + ", off_ticks: " + str( off_ticks))

            on_tick_bytes = on_ticks.to_bytes(2, 'little')
            off_tick_bytes = off_ticks.to_bytes(2, 'little')

            datatosend = datatosend + bytes([on_tick_bytes[0], on_tick_bytes[1], off_tick_bytes[0], off_tick_bytes[1]])


        #print(datatosend)
        self.__i2cdevice.i2c_write_bytes( datatosend)

    # --------------------------------------------------------------------------------------
    def sleep(self):
        """
        Put the device into a sleep state
        """
        oldmode = self.__read(MODE1_ADDRESS)
        newmode = oldmode | (1 << MODE1_SLEEP_BITNR)
        self.__write(MODE1_ADDRESS, newmode)

    # --------------------------------------------------------------------------------------
    def wake(self):
        """
        Wake the device from its sleep state
        """
        self.__write(MODE1_ADDRESS, 0x0000)
        newmode = 0x00a0
        self.__write(MODE1_ADDRESS, newmode)

    # --------------------------------------------------------------------------------------
    def is_sleeping(self):
        """
        Check the sleep status of the device
        :return: True or False
        :rtype: bool
        """
        regval = self.__read(MODE1_ADDRESS)
        if RoboUtil.checkbit(regval, MODE1_SLEEP_BITNR):
            return True
        else:
            return False

    #--------------------------------------------------------------------------------------
    def __set_pwm_freq(self, _freq, _calibration=-3):
        """
        Set the PWM frequency
        :param _freq: 40 to 1000
        :type _freq: int
        :param _calibration: optional integer value to offset oscillator errors. defaults to 0
        :raises ValueError: set_pwm_freq: freq out of range
        """
        if _freq < 40 or _freq > 1000:
            raise ValueError('set_pwm_freq: freq out of range')

        scaleval = 25000000.0               # 25MHz
        scaleval = scaleval / 4096.0        # 12-bit
        scaleval = scaleval / float(_freq)
        scaleval = scaleval - 1
        prescale = math.floor(scaleval + 0.5)
        prescale = prescale + _calibration

        print("scaleval: " + str(scaleval) + " Freq: " + str(_freq) + "Hz Prescaler: " + str(prescale))

        self.__freq = _freq

        self.sleep()
        self.__write(PRE_SCALE_ADDRESS, int(prescale))
        self.wake()

    def __convert_timeUs_to_tick(self, _time_wanted_us):
        time_per_tick = ((1.0 / self.__freq) / 4095.0) * 1000000
        actual_ticks = int(_time_wanted_us / time_per_tick)
        return actual_ticks

    def __do_invert_and_setDriverToPushPull(self):
        oldmode = self.__read(MODE2_ADDRESS)
        newmode = oldmode | (1 << MODE2_INVRT_BITNR)
        newmode = newmode | (1 << MODE2_OUTDRV_BITNR)
        self.__write(MODE2_ADDRESS, newmode)

    def __do_idle(self):
        self.__write(0x00, 0x00)

    # --------------------------------------------------------------------------------------
    def __write(self, reg, value):
        self.__i2cdevice.i2c_write_bytes(bytes([reg, value]))

    # --------------------------------------------------------------------------------------
    def __read(self, reg):
        return_value_array = bytearray(2)
        self.__i2cdevice.write_to_then_read_from(bytes([0x00, reg]), return_value_array)
        return return_value_array[0]

    # --------------------------------------------------------------------------------------



