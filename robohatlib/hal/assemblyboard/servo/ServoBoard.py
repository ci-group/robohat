"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

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
    from robohatlib.driver_ll.spi.SPIDevice import SPIDevice
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib.hal.assemblyboard.servo.ServoDriver import ServoDriver
    from robohatlib import RobohatConfig

except ImportError:

    print("Failed to resolve dependencies for Servoboard")
    raise

class ServoBoard:
    __servo_datas_list = None

    #--------------------------------------------------------------------------------------

    def __init__(self, _name:str, _i2c_device_servo: I2CDevice, _spi_device_servo_adc: SPIDevice):
        self.__name = _name
        self.__pwm = PCA9685(_i2c_device_servo)
        self.__servo_adc = MAX11137(_spi_device_servo_adc)
        self.__servoDriver = ServoDriver(self)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def init_servo_board(self, _servo_datas_list: []) -> None:
        """!
        @param _servo_datas_list:
        @return: None
        """

        self.__servo_datas_list = _servo_datas_list
        self.__servo_adc.init_adc()

        should_be_time = self._get_current_times_depending_current_angle()

        self.__pwm.init_pca9685(should_be_time)
        self.__servoDriver.start_driver()


    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def set_new_readout_vs_angle_formula(self, _servo_nr, _formula_a, _formula_b) -> None:
        """!
        Set new formula parameters for voltage angle conversion
        @param _servo_nr: wanted servo nr
        @param _formula_a: first part of linear formula
        @param _formula_b: second part of linear formula
        @return: None
        """

        if self.__servo_datas_list is not None:
            if len(self.__servo_datas_list) >= _servo_nr-1:
                self.__servo_datas_list[_servo_nr].set_new_readout_vs_angle_formula(_formula_a, _formula_b)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Get name of Servoboard
        @return: name
        """
        return self.__name

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down. Sets PWM to sleep
        @return: None
        """
        self.__servoDriver.stop_driver()
        self.put_to_sleep()


    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def set_servo_direct_mode(self, _mode:bool, _delay:float = RobohatConfig.DEFAULT_DELAY_BETWEEN_ACTION) -> None:
        """!
        Sets if the servos are periodically updated, or direct
        @param _mode: True, direct mode activated
        @param _delay, delay in update mode in seconds
        @return: None
        """
        self.__servoDriver.set_direct_mode(_mode)
        self.__servoDriver.set_delay(_delay)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_servo_is_direct_mode(self) -> bool:
        """!
        @return: if servo is NOT updated periodically
        """

        return self.__servoDriver.get_is_direct_mode()
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def update_servo_data(self, _wanted_angles: []) -> None:
        """!
        This is the return call of tge ServoDriver. Pushes the angles directly in the PWM chip
        @return: None
        """

        wanted_time_array = [0] * 16

        for i in range(0, 16):
            wanted_time_array[i] = self.__servo_datas_list[i].convert_angle_to_time(_wanted_angles[i])

        self.__pwm.set_on_time_all_channels(wanted_time_array)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_servo_us_time(self, _degree:float, _servo_nr:int=0) -> int:
        """!
        Get calculated time which is used to set the servo to the wanted degree
        @param _servo_nr
        @param _degree:
        @return: time in uS
        """

        return self.__servo_datas_list[_servo_nr].convert_angle_to_time(_degree)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_servo_is_single_servo_wanted_angle(self, _servo_nr: int) -> bool:
        """!
        Returns true if (previous) wanted angle the same as the angle of the servo

        @param _servo_nr: The sero index
        @return: bool
        """

        if _servo_nr < 0 or _servo_nr > 15:
            print("Error, requested servo number is not valid, should be 0 till 15")
            return False

        return self.__servoDriver.get_servo_is_single_servo_wanted_angle(_servo_nr)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def set_servo_single_angle(self, _servo_nr: int, _angle: float) -> None:
        """!
        Set the wanted angle of a servo
        @param _servo_nr: the servo nr (0 until 15)
        @param _angle: the wanted angle
        """

        if _servo_nr < 0 or _servo_nr > 15:
            print("Error, requested servo number is not valid, should be 0 till 15")
            return

        servo_data: ServoData = self.__servo_datas_list[_servo_nr]
        if _angle < servo_data.get_min_angle() or _angle > servo_data.get_max_angle():
            print("Error, requested angle: " + str(_angle) + " is not valid: min: " + str(servo_data.get_min_angle()) + " max: " + str( servo_data.get_max_angle()))
            return

        self.__servoDriver.set_servo_single_angle(_servo_nr, _angle)

    #--------------------------------------------------------------------------------------

    def set_servo_multiple_angles(self, _wanted_angles: []) -> None:
        """!
        Sets all the angle of the servos
        @param _wanted_angles:  (should be a list of 16, servo 1 is array pos 0)
        @return: None
        """

        length: int = len(_wanted_angles)
        if length > 16:
            print("Error, servo list can't br bigger than 16")
            return

        for servo_nr in range(0, length):
            servo_data: ServoData = self.__servo_datas_list[servo_nr]
            wanted_angle:float = _wanted_angles[servo_nr]

            if wanted_angle < servo_data.get_min_angle() or wanted_angle > servo_data.get_max_angle():
                print("Error, requested angle: " + str(wanted_angle) + " is not valid: min: " + str(servo_data.get_min_angle()) + " max: " + str(servo_data.get_max_angle()))
                return

        self.__servoDriver.set_servo_multiple_angles(_wanted_angles)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_servo_single_angle(self, _servo_nr: int) -> float:
        """!
        Get angle of connected servo in degree or -1 when in error

        @param _servo_nr The servo nr wanted (starts at 1)
        @return angle or -1
        """

        if _servo_nr >= 0 and _servo_nr < 16:
            voltage_channel = self.get_servo_adc_single_channel(_servo_nr)
            angle_channel = self.__servo_datas_list[_servo_nr - 1].convert_voltage_to_angle(voltage_channel)
            if angle_channel < 0:
                print("Error, requested servo: " + str(_servo_nr) + " readout is not connected")
                return -1
            return angle_channel
        else:
            print("Error, requested servo number is not valid, should be 1 till 16")
            return -1

    #--------------------------------------------------------------------------------------

    def get_servo_multiple_angles(self) -> []:
        """!
        Gets all the angle of the servos (Returns a list of 16, servo 0 is array pos 0)
        @return list of degrees
        """

        angle_list = [0] * 16
        for servo_nr in range(0, 16):
            voltage_adc_channel = self.__servo_adc.get_readout_adc_servo_nr(servo_nr)
            if voltage_adc_channel > 0.2:
                angle_list[servo_nr] = self.__servo_datas_list[servo_nr].convert_voltage_to_angle(voltage_adc_channel)
            else:
                angle_list[servo_nr] = -1
        return angle_list

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def set_update_value(self, _update_value: int) -> None:
        """!
        Set value which is used to add or subtract from current pos
        """
        if self.__servoDriver is not None:
            self.__servoDriver.set_update_value(_update_value)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_servo_adc_single_channel(self, _servo_nr: int) -> float:
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

    def _get_current_times_depending_current_angle(self) -> []:
        current_angles = self.get_servo_multiple_angles()
        should_be_time = [0] * 16
        for i in range(0, 16):
            angle = current_angles[i]
            if angle == -1:
                angle = 90
            should_be_time[i] = self.__servo_datas_list[i].convert_angle_to_time(angle)

        return should_be_time

    #--------------------------------------------------------------------------------------

    def get_servo_adc_multiple_channels(self) -> []:
        """!
        @return list of voltages of the angle of all the servos in volt Returns 16 elements
        """
        return self.__servo_adc.get_readout_adc_multiple_channels()

    #--------------------------------------------------------------------------------------

    def get_servo_is_connected(self, _servo_nr: int) -> bool:
        """!
        Checks if servo is connected. Returns False when not connected

        @param _servo_nr The servo nr
        @return: Returns False when not connected
        """
        value = self.get_servo_adc_single_channel(_servo_nr)
        if value < 0.2:
            return False
        else:
            return True

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
            self.__servo_datas_list[_servo_nr - 1].set_running_parameters(_min_time, _max_time, _running_degree, _offset_degree, _formula_a, _formula_b)
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

    def put_to_sleep(self) -> None:
        """!
        Put the device into a sleep state
        @return: None
        """
        self.__servoDriver.put_to_sleep()
        self.__pwm.put_to_sleep()

    #--------------------------------------------------------------------------------------

    def wake_up(self) -> None:
        """!
        Wakes up device
        @return: None
        """
        self.__pwm.wake_up()
        self.__servoDriver.wake_up()

    #--------------------------------------------------------------------------------------

    def are_servos_sleeping(self) -> bool:
        """!
        Get if Servos are sleeping
        @return: (bool) returns True when servos are sleeping
        """
        return self.__pwm.is_sleeping()

    #--------------------------------------------------------------------------------------
