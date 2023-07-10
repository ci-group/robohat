#!/usr/bin/python3
try:
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
except ImportError:
    print("Failed to import IOExpanderDef")
    raise

class IOExpanderDef:

    def __init__(self, _name, _i2c_device_definition:I2CDeviceDef, _gpio_pin:int, _interrupt_settings, _callback_function = None):
        """!
        @param _name:
        @param _i2c_device_definition:
        @param _gpio_pin:
        @param _interrupt_settings:
        @param _callback_function:
        """
        self.__name = _name
        self.__i2c_device_definition = _i2c_device_definition
        self.__gpio_pin = _gpio_pin
        self.__interrupt_settings = _interrupt_settings
        self.__callback_function = _callback_function

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """
        name of this definition
        :return: name
        """
        return self.__name

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

    def set_callback_function(self, _callback_function) -> None:
        """!
        @param _callback_function: new interrupt callback
        @return: None
        """
        self.__callback_function = _callback_function

    # --------------------------------------------------------------------------------------

    def get_callback_function(self):
        """!
        get the callback_function:
        @return: callback_function
        """
        return self.__callback_function

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

