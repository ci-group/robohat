try:
    from robohatlib.drivers.LIS3MDL import LIS3MDL
    from robohatlib.drivers.LSM6DS33 import LSM6DS33
    from typing import Tuple
except ImportError:
    print("Failed to import dependencies for IMU")
    raise


class IMU:
    def __init__(self, _iomanager, _imu_def):
        lis3mdl_i2c_def = _imu_def.get_lis3mdl_i2c_device_def()
        i2c_device_lis3ml = _iomanager.get_i2c_device(lis3mdl_i2c_def)
        self.__lis3ml = LIS3MDL(i2c_device_lis3ml)

        lsm6ds33_i2c_def = _imu_def.get_lsm6ds33_i2c_device_def()
        i2c_device_lsm6ds33 = _iomanager.get_i2c_device(lsm6ds33_i2c_def)
        self.__lsm6ds33 = LSM6DS33(i2c_device_lsm6ds33)

    # --------------------------------------------------------------------------------------

    def init_imu(self) -> None:
        """!
        Initializes the IMU

        Mandatory

        @return None
        """

        self.__lis3ml.init_LIS3MDL()
        self.__lsm6ds33.init_LSM6DS33()

    # --------------------------------------------------------------------------------------

    def do_imu_test(self):
        #self.lis3ml.do_test()
        self.__lsm6ds33.do_test()

    # --------------------------------------------------------------------------------------

    def get_magnetic_fields(self) -> Tuple[float, float, float]:
        """!
        Get the magnetic fields
        @return: (Typle x,y,z)  magnetic fields
        """
        return self.__lis3ml.get_magnetic_fields()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_acceleration(self) -> Tuple[float, float, float]:
        """!
        Get the acceleration fields
        @return: (Typle x,y,z)  acceleration fields
        """
        return self.__lsm6ds33.get_acceleration()

    # --------------------------------------------------------------------------------------

    def get_gyro(self) -> Tuple[float, float, float]:
        """!
        Get the gyro fields
        @return: (Typle x,y,z)  gyro fields
        """
        return self.__lsm6ds33.get_gyro()

    # --------------------------------------------------------------------------------------