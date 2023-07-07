# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class ServoData:
    """
    Storage of servo data.
    Each servo can have its own parameters. So different servos can be used
    __servo_nr: int = 1
    __min_time: float = 500
    __max_time: float = 2500
    __running_degree: float = 180
    __offset_degree = 0
    """

    # --------------------------------------------------------------------------------------

    def __init__(self, _servo_nr: int, _min_time: float, _max_time: float, _running_degree: float,
                 _offset_degree: float, _formula_a: float, _formula_b: float) -> None:
        """!
        The ServoData base class initializer.

        @param _servo_nr: servo nr (should be 1-16 on assembly 1 or 17-32 on assembly 2
        @param _min_time: PWM time of servo at minimum pos (something like 500 uS)
        @param _max_time: PWM time of servo at maximum pos (something like 2500 uS)
        @param _running_degree: Range of degree of servo (something like 180 degree)
        @param _offset_degree: Offset of the servo (should be 0)
        @param _formula_a: First parameter of formula, servo measure-voltage to angle
        @param _formula_b: Second parameter of formula, servo measure-voltage to angle

        @return: An instance of the ServoData class
        """

        self.__servo_nr = _servo_nr
        self.__min_time = _min_time
        self.__max_time = _max_time
        self.__running_degree = _running_degree
        self.__offset_degree = _offset_degree
        self.__formula_a = _formula_a
        self.__formula_b = _formula_b

    # --------------------------------------------------------------------------------------

    def convert_angle_to_time(self, _angle: float) -> float:
        """!
        Converts angle to time for PWM servo
        @_angle: the angle of the servo
        @return: (float) time in uS
        """

        time = (((self.__max_time - self.__min_time) / self.__running_degree) * (
                    _angle - self.__offset_degree)) + self.__min_time
        return time

    # --------------------------------------------------------------------------------------

    def get_servo_channel_nr(self) -> int:
        """!
         get servo nr of this class

         @return: (int), servo nr
         """
        return self.__servo_nr

    # --------------------------------------------------------------------------------------

    def set_running_parameters(self, _min_time: float, _max_time: float, _running_degree: float) -> None:
        """
        Sets new parameters to adjust servo time

        @return: None
        """

        self.__min_time = _min_time
        self.__max_time = _max_time
        self.__running_degree = _running_degree

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def convert_voltage_to_angle(self, _current_voltage: float) -> float:
        """
        converts voltage (measured by a adc, connected to the servo) to angle in degree

        formula determined by parameters defined in contructor

        y = ax + b , a = self._formula_a, b = self._formula_b,
        angle = self.__running_degree / (self.__max_degree_voltage_adc - self.__min_degree_voltage_adc ) * (_current_voltage - self.__min_degree_voltage_adc) - self.__offset_degree

        @_current_voltage voltage from servo, in volt
        @return: (float) angle in degree
        """

        angle = (self.__formula_a * _current_voltage) + self.__formula_b
        return angle

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
