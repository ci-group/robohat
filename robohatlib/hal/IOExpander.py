"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.drivers.MCP23008 import MCP23008
except ImportError:
    print("Failed to import MCP23008")
    raise

try:
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.IOExpanderDef import IOExpanderDef
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder
    from robohatlib.driver_ll.IOHandler import IOHandler
    from robohatlib.driver_ll.datastructs.IOStatus import IOStatus

except ImportError:
    print("Failed to import dependencies for IOExpander")
    raise

class IOExpander:
    """!
    IO expander class based on a MCP23008
    """
    #--------------------------------------------------------------------------------------

    def __init__(self, _iohandler:IOHandler, _io_expander_def:IOExpanderDef, _sw_io_expander:int):
        """!
        Constructor of IO expander
        @param _iohandler: the IO handler, connection to all the IO
        @param _io_expander_def: definition of this IO expander
        @param _sw_io_expander: offset of i2c base address
        """
        i2c_device_definition = _io_expander_def.get_i2c_device_definition()
        i2c_device_definition.set_i2c_offset_address(_sw_io_expander)
        i2c_device = _iohandler.get_i2c_device(i2c_device_definition)

        self.__gpi_interrupt_definition = None

        if i2c_device is not None:
            if _io_expander_def.get_callbackholder() is not None:
                self.__gpi_interrupt_definition = GPIInterruptDef(_io_expander_def.get_name(), _io_expander_def.get_gpio_pin(), InterruptTypes.INT_BOTH, _io_expander_def.get_callbackholder())
                _iohandler.register_interrupt(self.__gpi_interrupt_definition)

            self.__expander = MCP23008(i2c_device, _io_expander_def)
        else:
            self.__expander = None

    #--------------------------------------------------------------------------------------
    def init_io_expander(self) -> None:
        """!
        Initializes the io expander (Mandatory)

        @return -> None:
        """

        if self.__expander is not None:
            self.__expander.init_mcp23008()

    #--------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down
        @return: None
        """
        if self.__expander is not None:
            self.__expander.exit_program()

    #--------------------------------------------------------------------------------------

    def set_io_expander_direction(self, _io_nr:int, _direction: ExpanderDir) -> IOStatus:
        """!
        @param _io_nr: gpio pin nr
        @param _direction:     ExpanderDir.OUTPUT or  ExpanderDir.INPUT = 1
        @return: IOStatus
        """
        if self.__expander is not None:
            if self.__check_if_expander_io_is_available(_io_nr) is True:
                if  _direction is ExpanderDir.OUTPUT:
                    wanted_pin_value = 0
                else:
                    wanted_pin_value = 1
                self.__expander.set_pin_direction(_io_nr, wanted_pin_value)
                print("IO: Setting dir: " + str(_io_nr) + " <> " + str(wanted_pin_value))
                return IOStatus.IO_OK
            else:
                return IOStatus.IO_FAILED
        else:
            return IOStatus.IO_FAILED

    #--------------------------------------------------------------------------------------

    def get_io_expander_direction(self, _io_nr:int) -> ExpanderDir:
        if self.__expander is not None:
            if self.__check_if_expander_io_is_available(_io_nr) is True:
               value = self.__expander.get_pin_direction(_io_nr)
               if value == 0:
                   return ExpanderDir.OUTPUT
               else:
                   return ExpanderDir.INPUT
            else:
                return ExpanderDir.INVALID

    #--------------------------------------------------------------------------------------

    def set_io_expander_output(self, _io_nr:int, _status:ExpanderStatus) -> IOStatus:
        """!
        Set the output status of an io pin of the IO expander

        Note. direction of the pin must be an Output

        @param _io_nr io nr
        @param _status the status o the pin

        @return IOStatus
        """

        if self.__expander is not None:
            if self.__check_if_expander_io_is_available(_io_nr) is True:
                if self.get_io_expander_direction(_io_nr) == ExpanderDir.OUTPUT:
                    wanted_pin_value = 0
                    if  _status is ExpanderStatus.HIGH:
                        wanted_pin_value = 1
                    self.__expander.set_pin_data(_io_nr, wanted_pin_value)
                    return IOStatus.IO_OK
                else:
                    print("IOExpander: Can not write to an input pin")
                    return IOStatus.IO_FAILED
            else:
                return IOStatus.IO_FAILED
        else:
            return IOStatus.IO_FAILED

    #--------------------------------------------------------------------------------------

    def get_io_expander_input(self, _io_nr:int) -> ExpanderStatus:
        """!
        get the input status of an io pin of the IO expander

        Note. direction of the pin must be an Input

        @param _io_nr io nr

        @return status of the pin
        """
        if self.__expander is not None:
            if self.__check_if_expander_io_is_available(_io_nr) is True:
                if self.get_io_expander_direction(_io_nr) == ExpanderDir.INPUT:
                    value = self.__expander.get_pin_data(_io_nr)
                    if value == 0:
                        return ExpanderStatus.LOW
                    else:
                        return ExpanderStatus.HIGH
                else:
                    print("Can not read from an output pin: " + str(_io_nr))
        return ExpanderStatus.INVALID

    #--------------------------------------------------------------------------------------

    def reset_interrupt(self, _io_nr:int) -> None:
        """!
        @param _io_nr:
        @return: None
        """
        self.__expander.reset_interrupts()

    #--------------------------------------------------------------------------------------

    def __check_if_expander_io_is_available(self, _io_nr:int) -> bool:
        """!
        Checks if the IO is available, True if avaible

        @param _io_nr: pint n of the GPIO
        @return: bool
        """

        if self.__expander is None or _io_nr not in range(0, 8):
            print("io pin not available. Must between 0 until 7")
            return False
        return True

    #-------------------------------------------------------------------------------------

    def set_io_expander_int_callback_function(self, _callback_function) -> None:
        """!
        Set new callback function which will be executed when an interrupt triggers
        @param _callback_function: the callback function
        @return: None
        """
        if self.__gpi_interrupt_definition is not None:
            callbackholder:InterruptCallbackHolder = self.__gpi_interrupt_definition.get_callbackholder()
            callbackholder.set_callback_function(_callback_function)

    #-------------------------------------------------------------------------------------

    def set_io_expander_int_release_function(self, _release_int_function) -> None:
        """!
        Set new callback function which will be executed after the int callback function is executed, to reset the interrupt routine
        @param _release_int_function: the callback function
        @param _release_int_function:
        @return: None
        """
        if self.__gpi_interrupt_definition is not None:
            callbackholder:InterruptCallbackHolder = self.__gpi_interrupt_definition.get_callbackholder()
            callbackholder.set_release_int_release_function(_release_int_function)

    #-------------------------------------------------------------------------------------