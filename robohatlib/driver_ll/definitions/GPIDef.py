"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

class GPIDef:
    """!
    Definition of an GPIO defined as an input pin
    """

    def __init__(self, _name: str, _gpi_pin_nr: int):
        """!
        @param _name: name of this definition
        @param _gpi_pin_nr: GPIO pin nr
        """

        self.__name = _name
        self.__gpi_pin_nr = _gpi_pin_nr

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        @return: name of this definition
        """

        return self.__name

    # --------------------------------------------------------------------------------------

    def get_gpi_pin_nr(self) -> int:
        """!

        @return: io nr
        """
        return self.__gpi_pin_nr

    # --------------------------------------------------------------------------------------

