"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

class GPOPWMDef:
    """!
    Definition of an GPIO defined as an PWM output pin
    """

    def __init__(self, _name: str, _gpo_pin_nr: int, _freq, _duty_cycle:int):
        """!
        @param _name: name of this definition
        @aram _gpo_pin_nr:  GPIO pin nr
        @param _freq:  frequency in HZ
        @param _duty_cycle: Duty cycle in %
        """
        self.__name = _name
        self.__gpo_pin_nr = _gpo_pin_nr
        self.__freq = _freq
        self.__duty_cycle = _duty_cycle

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        name of this definition
        @return:  name of this definition
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_gpo_pin_nr(self) -> int:
        """!
        returns op pin nr
        @return: io pin nr
        """

        return self.__gpo_pin_nr

    # --------------------------------------------------------------------------------------

    def get_freq(self) -> int:
        """!
        returns frequency in Hz
        @return: frequency
        """
        return self.__freq

    # --------------------------------------------------------------------------------------

    def get_duty_cycle(self):
        """!
        returns duty cycle in %
        @return: duty cycle
        """
        return self.__duty_cycle

    # --------------------------------------------------------------------------------------
