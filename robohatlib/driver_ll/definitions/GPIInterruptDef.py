#!/usr/bin/python3
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

    def get_callbackholder(self):
        return self.__callbackholder

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # # --------------------------------------------------------------------------------------
    # @classmethod
    # def from_mcp23008_interrupt_definition(cls, _mcp_interrupt_definition):
    #     # if from mcp, type is always rising
    #     if _mcp_interrupt_definition is None:
    #         return None
    #
    #     return cls(_mcp_interrupt_definition.get_name(), _mcp_interrupt_definition.get_gpio_pin(), InterruptTypes.INT_BOTH, _mcp_interrupt_definition.get_callback_function())
    #
    # # --------------------------------------------------------------------------------------
    # # --------------------------------------------------------------------------------------
    # # --------------------------------------------------------------------------------------
    #
    # def __repr__(self):
    #     return (
    #         f"{self.__class__.__name__}"
    #         f"(name={self.__name}, gpio_pin={self.__gpio_pin}, interrupt_type_port={self.__interrupt_type_port}, callback_function={self.__callbackholder})"
    #     )

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

