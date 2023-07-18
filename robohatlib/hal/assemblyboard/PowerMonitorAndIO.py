from __future__ import annotations

try:
    from robohatlib.drivers.MCP23008 import MCP23008
    import time, threading
except ImportError:
    print("Failed to resolve dependencies for PowerMonitorAndIO")
    raise

try:
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.driver_ll.definitions.MCPInterruptDef import MCPInterruptDef
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.IOExpanderDef import IOExpanderDef
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib import Robohat_config
    from robohatlib.driver_ll.IOHandler import IOHandler
    from robohatlib.helpers.RoboUtil import RoboUtil

except ImportError:
    print("Failed to resolve dependencies for PowerMonitorAndIO")
    raise

class PowerMonitorAndIO:


    def __init__(self, _iohandler: IOHandler, _power_io_expander_def: IOExpanderDef, _sw_power_io_expander: int, _name_of_assembly:str = "" ):
        i2c_device_definition = _power_io_expander_def.get_i2c_device_definition()

        newname = i2c_device_definition.get_basename() + "_" + _name_of_assembly
        i2c_device_definition.set_name(newname)

        i2c_device_definition.set_i2c_offset_address(_sw_power_io_expander)
        i2c_device = _iohandler.get_i2c_device(i2c_device_definition)

        self.__interrupt = None
        self.__interrupt_type = None

        if i2c_device is not None:
            if _power_io_expander_def.get_callbackholder() is not None:
                self.__interrupt_type = _power_io_expander_def.get_callbackholder().get_interrupt_type()
                gpi_interrupt_definition = GPIInterruptDef(_power_io_expander_def.get_name(),
                                                           _power_io_expander_def.get_gpio_pin(),
                                                           _power_io_expander_def.get_callbackholder().get_interrupt_type(),
                                                           _power_io_expander_def.get_callbackholder())
                self.__interrupt = _iohandler.register_interrupt(gpi_interrupt_definition)

            self.__io_device = MCP23008(i2c_device, _power_io_expander_def)
        else:
            self.__io_device = None

        self.__signaling_device = None
        self.__reset_timerIsRunning = False
        self.disable_retry_timer_callback = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down
        @return: None
        """
        self.disable_retry_timer_callback = True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def init_power_monitor_and_io(self) -> None:
        """!
        Init power monitor
        Mandatory
        @return: None
        """
        if self.__io_device is not None:
            self.__io_device.init_mcp23008()

    # --------------------------------------------------------------------------------------

    def is_power_good(self, _power_channel: int) -> bool:
        """!
        Replies if DC/DC channel is ok
        @param _power_channel: Wanted channel
        @return: bool
        """
        value = self.get_io_expander_input(_power_channel)
        if value is 0:
            return False
        else:
            return True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_io_expander_direction(self, _io_nr:int) -> ExpanderDir | None:
        """!
        get the direction of the IO pin

        @param _io_nr io nr
        @return ExpanderDir or none
        """

        if self.__io_device is None:
            return

        if self.__check_if_expander_io_is_available(_io_nr) is True:
            value = self.__io_device.get_pin_data(_io_nr)
            if value is 0:
                return ExpanderDir.OUTPUT
            else:
                return ExpanderDir.INPUT
        else:
            print("io pin not available for user")
            return None

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def set_io_expander_direction(self, _io_nr:int, _direction: ExpanderDir) -> None:
        """!
        Set the direction of the IO pin

        @param _io_nr io nr
        @param _direction, 0 = Pin is configured as an output, 1 = Pin is configured as an input
        @return none
        """

        if self.__io_device is None:
            return

        if self.__check_if_expander_io_is_available(_io_nr) is True:
            if _direction is ExpanderDir.OUTPUT:
                wanted_pin_value = 0
            else:
                wanted_pin_value = 1
            self.__io_device.set_pin_direction(_io_nr, wanted_pin_value)

    # --------------------------------------------------------------------------------------
    #todo check in io-pin is an output
    def set_io_expander_output(self, _io_nr:int, _value: ExpanderStatus) -> None:
        """!
        Set the output of an output pin, onto the desired value
        @param _io_nr: wanted io nr
        @param _value wanted value
        @return None
        """
        if self.__io_device is None:
            return

        if self.__check_if_expander_io_is_available(_io_nr) is True:
            if _value is ExpanderStatus.LOW:
                self.__io_device.set_pin_data(_io_nr, 0)
            else:
                self.__io_device.set_pin_data(_io_nr, 1)

    # --------------------------------------------------------------------------------------
    #todo check in io-pin is an input
    def get_io_expander_input(self, _io_nr:int) -> ExpanderStatus | None:
        """!
        Gets current value of the desired input pin
        @param _io_nr: io nr

        @return ExpanderStatus or None
        """

        if self.__io_device is None:
            return None

        if self.__check_if_expander_io_is_available(_io_nr) is True:
            value = self.__io_device.get_pin_data(_io_nr)
            if value is 0:
                return ExpanderStatus.LOW
            else:
                return ExpanderStatus.HIGH
        else:
            return None

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
            self.__signaling_device.signal_system_alarm("A DC / DC converter of an servo is shorted !")

    # --------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic
    def __check_if_expander_io_is_available(self, _io_nr:int) -> bool:
        """!
        Checks if IO nr is available for the user (the 0-3 are reserved for power monitor!!)
        @param _io_nr: io nr
        @return: True is IO is available, False is not
        """
        if _io_nr >= 4 and _io_nr <= 6:
            return True
        else:
            return False

    # --------------------------------------------------------------------------------------
    def power_monitor_and_io_int_callback(self, _gpi_nr: int) -> None:
        """!
        The interrupt callback. Will be triggered by an interrupt generated by MCP23008

        @param _gpi_nr (int) mr of the callback gpio pin
        @return None
        """

        interrupt_stats = self.__io_device.read_interrupt_status()
        if RoboUtil.check_bit(interrupt_stats, 0) is 1:
            print("Major error: power fail DC/DC 1")
        if RoboUtil.check_bit(interrupt_stats, 1) is 1:
            print("Major error: power fail DC/DC 2")
        if RoboUtil.check_bit(interrupt_stats, 2) is 1:
            print("Major error: power fail DC/DC 3")
        if RoboUtil.check_bit(interrupt_stats, 3) is 1:
            print("Major error: power fail DC/DC 4")

        if self.__signaling_device is not None:
            self.__signaling_device.signal_system_alarm()
        else:
            print("No signaling device")

    # --------------------------------------------------------------------------------------

    def power_monitor_and_io_int_reset_routine(self, _gpi_nr: int) -> None:
        """!
        This routine will be called to reset the interrupt handler of the MCP23008
        @param _gpi_nr: IO nr of the caller
        @return: None
        """
        if self.__interrupt is not None:
            self.__interrupt.remove_event_detection()

        timer = threading.Timer(10, self.__reset_timer_callback)
        timer.start()

    # --------------------------------------------------------------------------------------

    def __reset_timer_callback(self) -> None:
        if self.__io_device is None:
            return

        if self.disable_retry_timer_callback is True:
            return

        port_value = self.__io_device.get_port_data() and 0x7f
        #print("--> " + hex(port_value) )
        if port_value > 0:
            #print("Not able to clear !!!!, power fail is present")
            timer = threading.Timer(10, self.__reset_timer_callback)
            timer.start()
        else:
            if self.__io_device is not None:
                 self.__io_device.reset_interrupts()

    # --------------------------------------------------------------------------------------

