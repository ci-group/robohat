WHO_AM_I = 0x0F

CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
CTRL_REG4 = 0x23
CTRL_REG5 = 0x24

STATUS_REG = 0x27
OUT_X_L = 0x28
OUT_X_H = 0x29
OUT_Y_L = 0x2A
OUT_Y_H = 0x2B
OUT_Z_L = 0x2C
OUT_Z_H = 0x2D
TEMP_OUT_L = 0x2E
TEMP_OUT_H = 0x2F
INT_CFG = 0x30
INT_SRC = 0x31
INT_THS_L = 0x32
INT_THS_H = 0x33

_GAUSS_TO_UT = 100

import time
from typing import Tuple

try:
    from robohatlib.helpers.RoboUtil import RoboUtil
except ImportError:
    print("Failed to import RoboUtil")
    raise


#   Full-scale (G), Gain@16-bit (LSB/Gauss)
#   4 	            6842
#   8 	            3421
#   12 	            2281
#   16 	            1711


CTRL_REG2_GAIN_BITNR =    5 # FS1 and FS2, gain
GAIN_4  = [0,  4, 6442]
GAIN_8  = [1,  8, 3421]
GAIN_12 = [2, 12, 2281]
GAIN_16 = [3, 16, 1711]


#
#accX = rawAccX * accel_scale * SENSORS_GRAVITY_STANDARD / 1000;
#accY = rawAccY * accel_scale * SENSORS_GRAVITY_STANDARD / 1000;
#accZ = rawAccZ * accel_scale * SENSORS_GRAVITY_STANDARD / 1000;
#


class LIS3MDL:

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __init__(self, _i2cdevice):
        self.__i2cdevice = _i2cdevice

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def init_LIS3MDL(self) -> None:
        print("init LIS3MDL")

        self.__i2cdevice.i2c_write_register_byte(CTRL_REG1, 0x70)          # 0x70 = 0b01110000,, OM = 11 (ultra-high-performance mode for X and Y); DO = 100 (10 Hz ODR)
        self.set_gain(GAIN_4)                                               # 0x00 = 0b00000000,  FS = 00 (+/- 4 gauss full scale)
        self.__i2cdevice.i2c_write_register_byte(CTRL_REG3, 0x00)          # 0x00 = 0b00000000,  MD = 00 (continuous-conversion mode)
        self.__i2cdevice.i2c_write_register_byte(CTRL_REG4, 0x0C)          # 0x0C = 0b00001100,  OMZ = 11 (ultra-high-performance mode for Z)

        print("Found LIS3MDL with ID: " + hex(self.__i2cdevice.i2c_read_register_byte (WHO_AM_I) ) )

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_gain(self, _selected_gain_array) -> None:
        ctrl_reg2_value = RoboUtil.update_byte(0x00, CTRL_REG2_GAIN_BITNR, _selected_gain_array[0])
        self.__i2cdevice.i2c_write_register_byte(CTRL_REG2, ctrl_reg2_value)
        self.__fullscalegaus = _selected_gain_array[1]
        self.__gain_divider = _selected_gain_array[2]
        print(_selected_gain_array)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_test(self) -> None:
        mag_x, mag_y, mag_z = self.get_magnetic_fields()
        print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    """The processed magnetometer sensor values.
    A 3-tuple of X, Y, Z axis values in microteslas that are signed floats.
    """
    def get_magnetic_fields(self) -> Tuple[float, float, float]:        # Reads the 3 mag channels and stores them in vector m
        in_value_array = bytearray(1)
        in_value_array[0] = (OUT_X_L | 0x80)

        return_value_array = bytearray(6)
        self.__i2cdevice.write_to_then_read_from(in_value_array, return_value_array)

        x_raw = int(return_value_array[0] | return_value_array[1] << 8)
        y_raw = int(return_value_array[2] | return_value_array[3] << 8)
        z_raw = int(return_value_array[4] | return_value_array[5] << 8)

        x = self.__convert_raw_to_gaus_in_ut(x_raw)
        y = self.__convert_raw_to_gaus_in_ut(y_raw)
        z = self.__convert_raw_to_gaus_in_ut(z_raw)

        return x, y, z

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __convert_raw_to_gaus_in_ut(self, raw_measurement: int) -> float:
        return (raw_measurement / self.__gain_divider) * _GAUSS_TO_UT

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_fullscale_gaus(self) -> int:
        return self.__fullscalegaus

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_gain_divider(self) -> int:
        return self.__gain_divider

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------






