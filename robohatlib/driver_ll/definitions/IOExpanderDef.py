"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder
except ImportError:
    print("Failed to resolve dependencies for IOExpanderDef")
    raise

class IOExpanderDef:

    def __init__(self, _name, _i2c_device_definition: I2CDeviceDef, _gpio_pin:int, _interrupt_settings: [], _callbackholder : InterruptCallbackHolder = None):
        """!
        @param _name:
        @param _i2c_device_definition:
        @param _gpio_pin:
        @param _interrupt_settings:
        @param _callbackholder:
        """

        self.__basename = _name
        self.__name = _name
        self.__i2c_device_definition = _i2c_device_definition
        self.__gpio_pin = _gpio_pin
        self.__interrupt_settings = _interrupt_settings
        self.__callbackholder = _callbackholder

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        name of this definition
        @return: name
        """
        return self.__name

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_basename(self) -> str:
        """!
        Get original name created at constructor
        @return: basename
        """
        return self.__basename

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def set_name(self, _name) -> None:
        """!
        Set new name of definition
        @param _name:
        @return: None
        """

        self.__name = _name

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_i2c_device_definition(self) -> I2CDeviceDef:
        """!
        returns i2c_device_definition
        @return: i2c_device_definition
        """

        return self.__i2c_device_definition

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_gpio_pin(self) -> int:
        """!
        Returns gpio pin nr
        @return gpio pin nr
        """

        return self.__gpio_pin

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_interrupt_settings(self) -> []:
        """
        @return:  interrupt_settings
        """
        return self.__interrupt_settings

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_callbackholder(self, _callbackholder : InterruptCallbackHolder) -> None:
        """!
        @param _callbackholder: new interrupt callback
        @return: None
        """
        self.__callbackholder = _callbackholder

    # --------------------------------------------------------------------------------------

    def get_callbackholder(self) -> InterruptCallbackHolder:
        """!
        get the callback_function:
        @return: InterruptCallbackHolder
        """
        return self.__callbackholder

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

