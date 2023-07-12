#!/usr/bin/python3

try:
    from robohatlib.drivers.PCA9685 import PCA9685

except ImportError:
    print("Failed to import PCA9685")
    raise

try:
    from robohatlib.drivers.MAX11137 import MAX11137
except ImportError:
    print("Failed to import MAX11137")
    raise

try:
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
    from robohatlib.driver_ll.spi.SPI_Device import SPI_Device
except ImportError:
    print("Failed to resolve dependencies for Servoboard")
    raise

class ServoBoard:
    __servo_datas_array = None

    #--------------------------------------------------------------------------------------

    def __init__(self, i2c_device_servo: I2CDevice, _spi_device_servo_adc: SPI_Device):
        self.__pwm = PCA9685(i2c_device_servo)
        self.__servo_adc = MAX11137(_spi_device_servo_adc)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def init_servo_board(self, _servo_datas_array: []):

        self.__servo_datas_array = _servo_datas_array
        self.__pwm.init_pca9685()
        self.__servo_adc.init_adc()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down. Sets PWM to sleep
        @return: None
        """
        self.__pwm.sleep()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def set_servo_angle(self, _servo_nr: int, _wanted_angle: float) -> None:
        wanted_time = self.__servo_datas_array[_servo_nr - 1].convert_angle_to_time(_wanted_angle)
        self.__pwm.set_on_time_channel(_servo_nr, wanted_time)

    #--------------------------------------------------------------------------------------

    def get_servo_angle(self, _servo_nr: int) -> float:
        """!
        Get angle of connected servo in degree

        @param _servo_nr The servo nr wanted (starts at 1)
        @return angle of connected servo in degree
        """

        voltage_channel = self.get_servo_readout_adc_single_channel(_servo_nr)
        angle_channel = self.__servo_datas_array[_servo_nr - 1].convert_voltage_to_angle(voltage_channel)
        return angle_channel

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    def set_all_servos_angle(self, _wanted_angles: []) -> None:
        wanted_time_array = [0] * 16
        for i in range(0, 16):
            wanted_time_array[i] = self.__servo_datas_array[i].convert_angle_to_time(_wanted_angles[i])

        self.__pwm.set_on_time_all_channels(wanted_time_array)

    #--------------------------------------------------------------------------------------

    def get_all_servos_angle(self) -> []:
        """!
        @return angles of servos in degree
        """

        angle_array = [0] * 17
        for servo_nr in range(1, 17):
            voltage_adc_channel = self.__servo_adc.get_readout_adc_servo_nr(servo_nr)
            print("-->" + str(servo_nr) + " " + str(voltage_adc_channel) + " V")
            angle_array[servo_nr] = self.__servo_datas_array[servo_nr-1].convert_voltage_to_angle(voltage_adc_channel)

        return angle_array

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_servo_readout_adc_single_channel(self, _servo_nr: int) -> float:
        """!
        Get voltage of the potentiometer of the connected servo in vol

        @param _servo_nr The servo nr wanted (starts at 1)

        @return voltage of the potentiometer of the connected servo in volt
        """
        return self.__servo_adc.get_readout_adc_servo_nr(_servo_nr)

    #--------------------------------------------------------------------------------------

    def get_servo_is_connected(self, _servo_nr: int) -> bool:
        """!
        Checks if servo is connected. Returns False when not connected

        @param _servo_nr The servo nr
        @return: Returns False when not connected
        """

        value = self.get_servo_readout_adc_single_channel(_servo_nr)
        if value < 0.1:
            return False
        return True

    #--------------------------------------------------------------------------------------

    def get_readout_adc_multiple_channels(self) -> []:
        """!
        @return voltages of the potentiometer of all the servos in volt
        """
        return self.__servo_adc.get_readout_adc_mutiplechannels()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def change_servo_parameters(self, _servo_channel, _min_time, _max_time, _running_degree,  _offset_degree, _min_degree_voltage_adc, _max_degree_voltage_adc):
        self.__servo_datas_array[_servo_channel - 1].set_running_parameters(_min_time, _max_time, _running_degree, _offset_degree, _min_degree_voltage_adc, _max_degree_voltage_adc)
        return None

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    # begin, servo assemblyboard adcs functions --------------------------------------------------------------------------------------
    def reset_adc(self):
        return self.__servo_adc.reset_adc()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def sleep(self) -> None:
        """!
        Put the device into a sleep state

        @:return: None
        """
        self.__pwm.sleep()

    #--------------------------------------------------------------------------------------

    def wake(self) -> None:
        """!
        Wakes up device

        @:return: None
        """
        self.__pwm.wake()

    #--------------------------------------------------------------------------------------

    def is_servo_sleeping(self) -> bool:
        """
        Get if Servos are sleeping
        @:return: (bool) returns True when servos are sleeping
        """
        return self.__pwm.is_sleeping()

    #--------------------------------------------------------------------------------------
