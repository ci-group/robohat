"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

class LedDef:
    """!
    Definition of a LED device
    """
    def __init__(self, _name:str, _gpo_pin_nr:int):
        """!
        @param _name: name of this definition
        @param _gpo_pin_nr:
        """

        self.__name = _name
        self.__gpo_pin_nr = _gpo_pin_nr

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Return name of this definition
        @return: name of this definition
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_gpo_pin_nr(self) -> int:
        """!
        @return: GPIO pin nr
        """
        return self.__gpo_pin_nr

    # --------------------------------------------------------------------------------------

