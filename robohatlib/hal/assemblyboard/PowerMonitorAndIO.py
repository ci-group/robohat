
try:
    from robohatlib.drivers.MCP23008 import MCP23008
except ImportError:
    print("Failed to import MCP23008")
    raise

try:
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
except ImportError:
    print("Failed to resolve dependencies for PowerMonitorAndIO")
    raise

class PowerMonitorAndIO:
    def __init__(self, _i2c_device, _mcp_interrupt_definition=None):
        self.__iodevice = MCP23008(_i2c_device, _mcp_interrupt_definition)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def init_power_monitor(self) -> None:
        """!
        Init power monitor
        For future use
        @return: None
        """
        print("Init power monitor")

    # --------------------------------------------------------------------------------------

    def is_power_good(self, _powerchannel) -> bool:
        return True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_direction_io_expander(self, _io_nr:int, _direction) -> None:
        """
        Set the direction of the IO pin

        @param _io_nr io nr
        @param _direction, 0 = Pin is configured as an output, 1 = Pin is configured as an input
        @return none
        """

        if self.__checkifexpanderioisavailble(_io_nr) is True:
            if _direction is ExpanderDir.OUTPUT:
                wanted_pin_value = 0
            else:
                wanted_pin_value = 1
            self.__iodevice.set_pin_direction(_io_nr, wanted_pin_value)
        else:
            print("io pin not available for user")
    # --------------------------------------------------------------------------------------

    def set_output_io_expander(self, _io_nr:int, _bool_value) -> None:
        """
        @:param _io_nr: io nr
        @:return none
        """
        if self.__checkifexpanderioisavailble(_io_nr) is True:
            self.__iodevice.set_pin_data(_io_nr, _bool_value)
        else:
            print("io pin not available for user")

    # --------------------------------------------------------------------------------------

    def get_input_io_expander(self, _io_nr:int) -> int:
        """!
        @param _io_nr: io nr

        @return none
        """
        if self.__checkifexpanderioisavailble(_io_nr) is True:
            return self.__iodevice.get_pin_data(_io_nr)
        return 0

    # --------------------------------------------------------------------------------------

    def __checkifexpanderioisavailble(self, _io_nr:int) -> bool:
        """!
        Checks if IO nr is avaible for the user (the 0-3 are reserved for power monitor!!
        @param _io_nr: io nr
        @return: True is IO is available, False is not
        """
        if _io_nr in range(4, 7):
            return True
        return False

    # --------------------------------------------------------------------------------------
