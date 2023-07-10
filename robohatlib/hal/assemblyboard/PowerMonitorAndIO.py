
#todo corect PowerMonitorAndIO

try:
    from robohatlib.drivers.MCP23008 import MCP23008
except ImportError:
    print("Failed to import MCP23008")
    raise

try:
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.driver_ll.definitions.MCPInterruptDef import MCPInterruptDef
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder

    from robohatlib import Robohat_config
except ImportError:
    print("Failed to resolve dependencies for PowerMonitorAndIO")
    raise

class PowerMonitorAndIO:
    def __init__(self, _i2c_device: I2CDevice):
        self.__io_device = None
        # #new
        # io_expander_def = Robohat_config.SERVOASSEMBLY_EXPANDER_DEF
        #
        #
        # # at the default interrupt definition there are 2 callback added. one for the trigger, the second for the interrupt reset
        # callbackholder = InterruptCallbackHolder("powermonitorandio_callback_holder", self._io_expander_int_callback, self._io_expander_int_reset_routine, 250)
        # io_expander_def.set_callbackholder(callbackholder)
        #
        #
        # # i2c_device_definition = _io_expander_def.get_i2c_device_definition()
        # # i2c_device_definition.set_i2c_offset_address(_sw_io_expander)
        # # i2c_device = _iohandler.get_i2c_device(i2c_device_definition)
        #
        # # if i2c_device is not None:
        # #     if io_expander_def.get_callbackholder() is not None:
        # #         gpi_interrupt_definition = GPIInterruptDef(io_expander_def.get_name(), io_expander_def.get_gpio_pin(), InterruptTypes.INT_BOTH, io_expander_def.get_callbackholder() )
        # #         _iohandler.register_interrupt(gpi_interrupt_definition)
        #
        #
        # #servo_assembly_interrupt_def = MCPInterruptDef("servo_assembly_int", Robohat_config.SERVOASSEMBLY_COMMON_GPI, self._io_servo_assembly_callback)
        # self.__io_device = MCP23008(_i2c_device, io_expander_def)
        # self.__signaling_device = None

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

    def is_power_good(self, _power_channel: int) -> bool:
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

        if self.__io_device is None:
            return

        if self.__check_if_expander_io_is_availble(_io_nr) is True:
            if _direction is ExpanderDir.OUTPUT:
                wanted_pin_value = 0
            else:
                wanted_pin_value = 1
            self.__io_device.set_pin_direction(_io_nr, wanted_pin_value)
        else:
            print("io pin not available for user")
    # --------------------------------------------------------------------------------------

    def set_output_io_expander(self, _io_nr:int, _bool_value) -> None:
        """
        @:param _io_nr: io nr
        @:return none
        """
        if self.__io_device is None:
            return

        if self.__check_if_expander_io_is_availble(_io_nr) is True:
            self.__io_device.set_pin_data(_io_nr, _bool_value)
        else:
            print("io pin not available for user")

    # --------------------------------------------------------------------------------------

    def get_input_io_expander(self, _io_nr:int) -> int:
        """!
        @param _io_nr: io nr

        @return none
        """

        if self.__io_device is None:
            return 0

        if self.__check_if_expander_io_is_availble(_io_nr) is True:
            return self.__io_device.get_pin_data(_io_nr)
        return 0

    # --------------------------------------------------------------------------------------
    def add_signaling_device(self, _signaling_device) -> None:
        """!
        Adds device which will alarms the user
        @param _signaling_device:
        @return: Nome
        """
        self.__signaling_device = _signaling_device
    # --------------------------------------------------------------------------------------

    def _io_servo_assembly_callback(self, _gpi_nr):
        """!
        Alarms the user when an DC/DC converter shuts down

        @param _gpi_nr: mr of the callback gpio pin

        @return None
        """

        print("_io_servo_assembly_callback by: " + str(_gpi_nr))

        if self.__signaling_device is not None:
            self.__signaling_device.signal_system_alarm()

    # --------------------------------------------------------------------------------------


    def __check_if_expander_io_is_availble(self, _io_nr:int) -> bool:
        """!
        Checks if IO nr is available for the user (the 0-3 are reserved for power monitor!!
        @param _io_nr: io nr
        @return: True is IO is available, False is not
        """
        if _io_nr in range(4, 7):
            return True
        return False

    # --------------------------------------------------------------------------------------
    #todo alarma to user !
    def _io_expander_int_callback(self, _gpi_nr: int) -> None:
        """!
        Just a test callback, should be removed in the future

        @param _gpi_nr (int) mr of the callback gpio pin
        @return None
        """
        print("DCDC _io_expander_int_callback by: " + str(_gpi_nr))

    def _io_expander_int_reset_routine(self, _gpi_nr: int) -> None:
        """!
        This routine will be called to reset the interrupt handler of the MCP23008
        @param _gpi_nr: IO nr of the caller
        @return: None
        """
        if self.__io_device is None:
            return

        if self.__io_device is not None:
            self.__io_device.reset_interrupts()

    # --------------------------------------------------------------------------------------
