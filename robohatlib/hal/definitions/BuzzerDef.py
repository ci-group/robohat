"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

class BuzzerDef:
    """!
    Definition of a Buzzer
    """

    def __init__(self, _name, _gpo_pin_nr, _freq = 1000, _dutycycle = 50) -> None:
        """!
        Constructor of this buzzer class.

        @param _name: Unique name
        @param _gpo_pin_nr: GPIO pin nr connected to the buzzer.
        @param _freq: frequency in Hz, of the PWM signal
        @param _dutycycle: The duty cycle of the PWM signal in %, of the buzzer, default 50%
        """
        self.__name = _name
        self.__gpo_pin_nr = _gpo_pin_nr
        self.__freq = _freq
        self.__dutycycle = _dutycycle

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Returns the name of the buzzer

        @return str, name of the buzzer:
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_gpo_pin_nr(self) -> int:
        """!
        Returns the gpio pin nr of the connected buzzer

        @return: int, gpio pin nr, used as output
        """
        return self.__gpo_pin_nr

    # --------------------------------------------------------------------------------------

    def get_freq(self) -> int:
        """!
        Returns the frequency of the PWM signal of the Buzzer

        @return: int, frequency in Hz
        """
        return self.__freq

    # --------------------------------------------------------------------------------------

    def get_duty_cycle(self) -> int:
        """!
        Returns the duty cycle of the PWM signal of the Buzzer

        @return: duty cycle in %
        """
        return self.__dutycycle

    # --------------------------------------------------------------------------------------
