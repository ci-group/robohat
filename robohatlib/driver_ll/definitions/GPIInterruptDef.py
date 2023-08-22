"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder
except ImportError:
    print("Failed resolve dependencies for GPIInterruptDef")
    raise


class GPIInterruptDef:
    """!
    Definition of an GPIO defined as an interrupt input pin
    """

    def __init__(self, _name: str, _gpio_pin: int, _interrupt_type_port, _callbackholder:InterruptCallbackHolder = None):
        """
        @param _name:  name of this definition
        @param _gpio_pin:  GPIO pin nr
        @param _interrupt_type_port:
        @param _callbackholder:
        """

        self.__name = _name
        self.__gpio_pin = _gpio_pin
        self.__interrupt_type_port = _interrupt_type_port
        self.__callbackholder = _callbackholder

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

        @return: io nr of the gpi pin
        """
        return self.__gpio_pin

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_interrupt_type_port(self):
        return self.__interrupt_type_port

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_callbackholder(self) -> InterruptCallbackHolder:
        """!

        @return: InterruptCallbackHolder
        """
        return self.__callbackholder

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

