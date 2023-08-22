"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
except ImportError:
    raise ImportError("Failed to import needed dependencies for IMUDef")

class IMUDef:
    """!
    Definition of a IMU
    """

    def __init__(self, _name, _lis3mdl_i2c_device_def, _lsm6ds33_i2c_device_def):
        """!
        Constructor of IMUDef

        @param _name:  name of this definition
        @param _lis3mdl_i2c_device_def: The definition for th LIS3MDL
        @param _lsm6ds33_i2c_device_def: The definition for th LMS6D33
        """
        self.__name = _name
        self.__lis3mdl_i2c_device_def = _lis3mdl_i2c_device_def
        self.__lsm6ds33_i2c_device_def = _lsm6ds33_i2c_device_def

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Get name of this definition

        @return: (str) name of this definition
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_lis3mdl_i2c_device_def(self) -> I2CDeviceDef:
        """!
        Get definition for th LIS3MDL

        @return: get device definition for th LIS3MDL
        """
        return self.__lis3mdl_i2c_device_def

    # --------------------------------------------------------------------------------------

    def get_lsm6ds33_i2c_device_def(self) -> I2CDeviceDef:
        """!
        Get definition for th LMS6D33

        @return: get device definition for th LMS6D33
        """
        return self.__lsm6ds33_i2c_device_def

    # --------------------------------------------------------------------------------------

