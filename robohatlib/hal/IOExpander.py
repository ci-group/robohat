#!/usr/bin/python3
try:
    from robohatlib.drivers.MCP23008 import MCP23008
except ImportError:
    print("Failed to import MCP23008")
    raise

try:
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
    from robohatlib.driver_ll.definitions.IOExpanderDef import IOExpanderDef
    from robohatlib.driver_ll.IOHandler import IOHandler
except ImportError:
    print("Failed to import dependencies for IOExpander")
    raise


class IOExpander:

    #--------------------------------------------------------------------------------------
    def __init__(self, _iohandler:IOHandler, _io_expander_def:IOExpanderDef, _sw_io_expander:int):

        i2c_device_definition = _io_expander_def.get_i2c_device_definition()
        i2c_device_definition.set_i2c_offset_address(_sw_io_expander)
        i2c_device = _iohandler.get_i2c_device(i2c_device_definition)

        if i2c_device is not None:
            if _io_expander_def.get_callback_function() is not None:
                gpi_interrupt_definition = GPIInterruptDef.from_mcp23008_interrupt_definition(_io_expander_def)
                _iohandler.register_interrupt(gpi_interrupt_definition)

            self.__expander = MCP23008(i2c_device, _io_expander_def)
        else:
            self.__expander = None

    #--------------------------------------------------------------------------------------
    def init_io_expander(self) -> None:
        """
        Initializes the io expander

        Mandatory

        @return -> None:
        """

        if self.__expander is not None:
            self.__expander.init_mcp23008()

    #--------------------------------------------------------------------------------------
    def set_direction_io_expander(self, _io_nr:int, _direction: ExpanderDir) -> None:
        """!
        @param _io_nr: gpio pin nr
        @param _direction:     ExpanderDir.OUTPUT or  ExpanderDir.INPUT = 1
        @return: None
        """
        if self.__expander is not None:
            self.__check_if_expander_io_is_availble(_io_nr)
            if  _direction is ExpanderDir.OUTPUT:
                wanted_pin_value = 0
            else:
                wanted_pin_value = 1
            self.__expander.set_pin_direction(_io_nr, wanted_pin_value)

    #--------------------------------------------------------------------------------------

    def set_io_expander_output_status(self, _io_nr:int, _status) -> None:
        """!
        Set the output status of an io pin of the IO expander

        Note. direction of the pin must be an Output

        @param _io_nr io nr
        @param _status the status o the pin

        @return None
        """

        if self.__expander is not None:
            self.__check_if_expander_io_is_availble(_io_nr)

            wanted_pin_value = 0

            if  _status is ExpanderStatus.LOW:
                wanted_pin_value = 0

            self.__expander.set_pin_data(_io_nr, wanted_pin_value)

    #--------------------------------------------------------------------------------------

    def get_io_expander_input(self, _io_nr:int):
        """!
        get the input status of an io pin of the IO expander

        Note. direction of the pin must be an Input

        @param _io_nr io nr

        @return status of the pin or 0 when not available
        """
        if self.__expander is not None:
            self.__check_if_expander_io_is_availble(_io_nr)
            return self.__expander.get_pin_data(_io_nr)

        return 0

    #--------------------------------------------------------------------------------------

    def __check_if_expander_io_is_availble(self, _io_nr:int) -> None:
        """!
        Checks if the IO is available

        @param _io_nr: pint n of the GPIO
        @return: Nome
        @:raises exception when not available
        """

        if self.__expander is None or _io_nr not in range(0, 8):
            raise ValueError("only io0 till io7 are available")
