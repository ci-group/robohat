"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

class MCPInterruptDef:
    """!
    Definition of a MCPInterrupt device
    """
    def __init__(self, _name, _gpio_pin, _callback_function):
        """!

        @param _name:  name of this definition
        @param _gpio_pin:  GPIO pin nr
        @param _callback_function: the callback function
        """
        self.__name = _name
        self.__gpio_pin = _gpio_pin
        self.__callback_function = _callback_function

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Returns name of this definition

        @return: name of this definition
        """
        return self.__name

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_gpio_pin(self) -> int:
        """!
        Returns the gpio pin nr
        @return: GPIO pin nr
        """
        return self.__gpio_pin

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_callback_function(self):
        """!
        @return: callback_function
        """
        return self.__callback_function

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

