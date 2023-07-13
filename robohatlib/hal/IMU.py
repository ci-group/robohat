from __future__ import annotations

try:
    from robohatlib.drivers.LIS3MDL import LIS3MDL
    from robohatlib.drivers.LSM6DS33 import LSM6DS33
    from typing import Tuple
except ImportError:
    print("Failed to import dependencies for IMU")
    raise


class IMU:
    def __init__(self, _io_handler, _imu_def):
        lis3mdl_i2c_def = _imu_def.get_lis3mdl_i2c_device_def()
        i2c_device_lis3ml = _io_handler.get_i2c_device(lis3mdl_i2c_def)

        if i2c_device_lis3ml is not None:
            self.__lis3ml = LIS3MDL(i2c_device_lis3ml)
        else:
            self.__lis3ml = None

        lsm6ds33_i2c_def = _imu_def.get_lsm6ds33_i2c_device_def()
        i2c_device_lsm6ds33 = _io_handler.get_i2c_device(lsm6ds33_i2c_def)

        if i2c_device_lsm6ds33 is not None:
            self.__lsm6ds33 = LSM6DS33(i2c_device_lsm6ds33)
        else:
            self.__lsm6ds33 = None

    # --------------------------------------------------------------------------------------

    def init_imu(self) -> None:
        """!
        Initializes the IMU

        Mandatory

        @return None
        """

        if self.__lis3ml is not None:
            self.__lis3ml.init_LIS3MDL()

        if self.__lsm6ds33 is not None:
            self.__lsm6ds33.init_LSM6DS33()


    # --------------------------------------------------------------------------------------
    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down
        @return: None
        """

    # --------------------------------------------------------------------------------------

    def do_imu_test(self):
        if self.__lis3ml is not None:
            self.__lis3ml.do_test()

        if self.__lsm6ds33 is not None:
            self.__lsm6ds33.do_test()

    # --------------------------------------------------------------------------------------

    def get_magnetic_fields(self) -> Tuple[float, float, float] | None:
        """!
        Get the magnetic fields or None when not available
        @return: (Tuple x,y,z)  magnetic fields or None
        """

        if self.__lis3ml is not None:
            return self.__lis3ml.get_magnetic_fields()
        return None

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_acceleration(self) -> Tuple[float, float, float] | None:
        """!
        Get the acceleration fields or None when not available
        @return: (Tuple x,y,z)  acceleration fields or None
        """

        if self.__lsm6ds33 is not None:
            return self.__lsm6ds33.get_acceleration()
        return None

    # --------------------------------------------------------------------------------------

    def get_gyro(self) -> Tuple[float, float, float] | None:
        """!
        Get the gyro fields or None when not available
        @return: (Tuple x,y,z)  gyro fields or None
        """

        if self.__lsm6ds33 is not None:
            return self.__lsm6ds33.get_gyro()
        return None

    # --------------------------------------------------------------------------------------