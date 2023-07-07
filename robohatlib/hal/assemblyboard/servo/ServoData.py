# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class ServoData:
    __servo_channel:int = 1
    __min_time:float = 500
    __max_time:float = 2500
    __running_degree:float = 180
    __offset_degree = 0
    # --------------------------------------------------------------------------------------

    def __init__(self, _servo_ch:int, _min_time:float, _max_time:float, _running_degree:float, _offset_degree:float, _formula_a:float, _formula_b:float) -> None:
        """
        The ServoData base class initializer.

        :param _servo_ch:
        :param _min_time:
        :param _max_time:
        :param _running_degree:
        :param _offset_degree:
        :param _formula_a:
        :param _formula_b:

        :return: An instance of the ServoData class
        """

        self.__servo_channel = _servo_ch
        self.__min_time = _min_time
        self.__max_time = _max_time
        self.__running_degree = _running_degree
        self.__offset_degree = _offset_degree
        self.__formula_a = _formula_a
        self.__formula_b = _formula_b

    # --------------------------------------------------------------------------------------

    def convert_angle_to_time(self, _angle: float) -> float:
        """
         converts angle to time for PWM servo

         :return: float
         """

        time = (((self.__max_time - self.__min_time) / self.__running_degree) * (_angle - self.__offset_degree) ) + self.__min_time
        return time

    # --------------------------------------------------------------------------------------

    def get_servo_channel_nr(self) -> int:
        """
         get servo nr of this class

         :return: int, channel nr
         """
        return self.__servo_channel

    # --------------------------------------------------------------------------------------

    def set_running_parameters(self, _min_time:float, _max_time:float, _running_degree:float) -> None:
        """
         set new parameters to adjust servo time

         :return: None
         """
        self.__min_time = _min_time
        self.__max_time = _max_time
        self.__running_degree = _running_degree

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def convert_voltage_to_angle(self, _current_voltage:float) -> float:
        """
         converts voltage (measured by a adc, connected to the servo) to angle in degree

         formula determined by parameters defined in contructor

         y = ax + b , a = self._formula_a, b = self._formula_b,
         angle = self.__running_degree / (self.__max_degree_voltage_adc - self.__min_degree_voltage_adc ) * (_current_voltage - self.__min_degree_voltage_adc) - self.__offset_degree

         :return: float
         """

        angle = (self.__formula_a * _current_voltage) + self.__formula_b
        return angle

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------