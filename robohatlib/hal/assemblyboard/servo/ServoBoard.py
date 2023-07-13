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
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
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

    def set_servo_angle(self, _servo_nr: int, _angle: float) -> None:
        if _servo_nr >= 0 and _servo_nr < 16:
            servo_data:ServoData = self.__servo_datas_array[_servo_nr]

            if _angle >= servo_data.get_min_angle() or _angle <= servo_data.get_max_angle():
                wanted_time = servo_data.convert_angle_to_time(_angle)
                self.__pwm.set_on_time_channel(_servo_nr, wanted_time)
            else:
                print("Error, requested angle is not valid: min: " + str(servo_data.get_min_angle()) + " max: " + str(servo_data.get_max_angle()) )
        else:
            print("Error, requested servo number is not valid, should be 0 till 15")
    #--------------------------------------------------------------------------------------

    def get_servo_angle(self, _servo_nr: int) -> float:
        """!
        Get angle of connected servo in degree or -1 when in error

        @param _servo_nr The servo nr wanted (starts at 1)
        @return angle or -1
        """

        if _servo_nr >= 0 and _servo_nr < 16:
            voltage_channel = self.get_servo_readout_adc_single_channel(_servo_nr)
            angle_channel = self.__servo_datas_array[_servo_nr - 1].convert_voltage_to_angle(voltage_channel)
            return angle_channel
        else:
            print("Error, requested servo number is not valid, should be 1 till 16")
            return -1

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    def set_all_servos_angle(self, _wanted_angles: []) -> None:
        """!
        Sets all the angle of the servos
        @param _wanted_angles:  (should be a array of 16, servo 1 is array pos 0)
        @return: None
        """
        wanted_time_array = [0] * 16
        for i in range(0, 16):
            wanted_time_array[i] = self.__servo_datas_array[i].convert_angle_to_time(_wanted_angles[i])
        self.__pwm.set_on_time_all_channels(wanted_time_array)

    #--------------------------------------------------------------------------------------

    def get_all_servos_angle(self) -> []:
        """!
        Gets all the angle of the servos (Returns an array of 16, servo 0 is array pos 0)
        @return array of degrees
        """

        angle_array = [0] * 17
        for servo_nr in range(0, 16):
            voltage_adc_channel = self.__servo_adc.get_readout_adc_servo_nr(servo_nr)
            angle_array[servo_nr] = self.__servo_datas_array[servo_nr].convert_voltage_to_angle(voltage_adc_channel)

        return angle_array

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_servo_readout_adc_single_channel(self, _servo_nr: int) -> float:
        """!
        Get voltage of the potentiometer of the connected servo in volt or -1 when in error
        @param _servo_nr The servo nr wanted (starts at 01)
        @return voltage or -1
        """

        if _servo_nr >= 0 and _servo_nr < 16:
            return self.__servo_adc.get_readout_adc_servo_nr(_servo_nr)
        else:
            print("Error, requested servo number is not valid, should be 1 till 16")
            return -1

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
        else:
            return True

    #--------------------------------------------------------------------------------------

    def get_readout_adc_multiple_channels(self) -> []:
        """!
        @return voltages of the potentiometer of all the servos in volt
        """
        return self.__servo_adc.get_readout_adc_mutiplechannels()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def change_servo_parameters(self, _servo_nr:int, _min_time:float, _max_time:float, _running_degree:float,  _offset_degree:float, _formula_a:float, _formula_b:float) -> None:
        """!
         Sets new parameters to adjust servo time

        @param _servo_nr:  servo nr (should be 0-15)
        @param _min_time: PWM time of servo at minimum pos (something like 500 uS)
        @param _max_time: PWM time of servo at maximum pos (something like 2500 uS)
        @param _running_degree: Range of degree of servo (something like 180 degree)
        @param _offset_degree: Offset of the servo (should be 0)
        @param _formula_a:  First parameter of formula, servo measure-voltage to angle
        @param _formula_b: Second parameter of formula, servo measure-voltage to angle
        @return: None
        """

        if _servo_nr >= 0 and _servo_nr < 16:
            self.__servo_datas_array[_servo_nr - 1].set_running_parameters(_min_time, _max_time, _running_degree, _offset_degree, _formula_a, _formula_b)
        else:
            print("Error, requested servo number is not valid, should be 1 till 16")

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    # begin, servo assemblyboard adcs functions --------------------------------------------------------------------------------------
    def reset_adc(self) -> None:
        """!
        Resets the ADC which measures the angle of the servos
        @return: None
        """
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

    def are_servos_sleeping(self) -> bool:
        """!
        Get if Servos are sleeping
        @return: (bool) returns True when servos are sleeping
        """
        return self.__pwm.is_sleeping()

    #--------------------------------------------------------------------------------------
