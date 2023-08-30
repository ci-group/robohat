"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

from __future__ import annotations

try:
    from robohatlib.drivers.MCP23008 import MCP23008
except ImportError:
    print("Failed to import MCP23008 in PowerMonitorAndIO")
    raise

try:
    import time, threading
    from robohatlib.RobohatConfig import DEBUG
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.IOExpanderDef import IOExpanderDef
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder
    from robohatlib.driver_ll.IOHandler import IOHandler
    from robohatlib.driver_ll.datastructs.IOStatus import IOStatus
    from robohatlib.helpers.RoboUtil import RoboUtil
    from robohatlib.hal.assemblyboard.PowerMonitorTimer import PowerMonitorTimer

except ImportError:
    print("Failed to import dependencies for PowerMonitorAndIO")
    raise


class PowerMonitorAndIO:
    """!
    IO expander class based on a MCP23008
    """

    #--------------------------------------------------------------------------------------

    def __init__(self, _iohandler:IOHandler, _power_io_expander_def:IOExpanderDef, _sw_io_expander:int, _name_of_assembly:str = ""):
        """!
        Constructor of PowerMonitorAndIO
        @param _iohandler: the IO handler, connection to all the IO
        @param _power_io_expander_def: definition of this IO expander
        @param _sw_io_expander: offset of i2c base address
        @param _name_of_assembly: name of this assembly
        """
        i2c_device_definition = _power_io_expander_def.get_i2c_device_definition()

        newname = i2c_device_definition.get_basename() + "_" + _name_of_assembly
        i2c_device_definition.set_name(newname)

        i2c_device_definition.set_i2c_offset_address(_sw_io_expander)
        i2c_device = _iohandler.get_i2c_device(i2c_device_definition)

        self.__interrupt = None
        self.__interrupt_type = None
        self.__user_int_callback = None

        if i2c_device is not None:
            if _power_io_expander_def.get_callbackholder() is not None:
                self.__interrupt_type = _power_io_expander_def.get_callbackholder().get_interrupt_type()
                gpi_interrupt_definition = GPIInterruptDef(_power_io_expander_def.get_name(),
                                                           _power_io_expander_def.get_gpio_pin(),
                                                           _power_io_expander_def.get_callbackholder().get_interrupt_type(),
                                                           _power_io_expander_def.get_callbackholder())
                self.__interrupt = _iohandler.register_interrupt(gpi_interrupt_definition)

            self.__expander = MCP23008(i2c_device, _power_io_expander_def)
            self.__expander.set_interrupt_defaults(0x15)
        else:
            self.__expander = None

        self.__signaling_device = None
        self.__reset_timerIsRunning = False
        self.disable_retry_timer_callback = False

        self.__timer0 = PowerMonitorTimer(0, self, self.__expander, _name_of_assembly)
        self.__timer1 = PowerMonitorTimer(1, self, self.__expander, _name_of_assembly)
        self.__timer2 = PowerMonitorTimer(2, self, self.__expander, _name_of_assembly)
        self.__timer3 = PowerMonitorTimer(3, self, self.__expander, _name_of_assembly)

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
        self.disable_retry_timer_callback = True

        if self.__expander is not None:
            self.__expander.exit_program()

    # --------------------------------------------------------------------------------------

    def is_power_good(self, _power_channel: int) -> bool:
        """!
        Replies if DC/DC channel is ok
        @param _power_channel: Wanted channel
        @return: bool
        """
        value = self.get_io_expander_input(_power_channel)
        if value is ExpanderStatus.HIGH:
            return True
        else:
            return False

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
                #if DEBUG is True:
                #    print("PowerMon: Setting dir: " + str(_io_nr) + " <> " + str(wanted_pin_value))
                return IOStatus.IO_OK
            else:
                return IOStatus.IO_FAILED
        else:
            return IOStatus.IO_FAILED

    #--------------------------------------------------------------------------------------

    def get_io_expander_direction(self, _io_nr:int) -> ExpanderDir:
        """!
        get the direction of the IO pin

        @param _io_nr io nr
        @return ExpanderDir
        """

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
                    print("PowerMon: Can not write to an input pin")
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
        @param _io_nr: IO which is responsible for the interrupt
        @return: None
        """
        self.__expander.reset_interrupts()

    #--------------------------------------------------------------------------------------

    def add_signaling_device(self, _signaling_device) -> None:
        """!
        Adds device which will alarms the user
        @param _signaling_device:
        @return: Nome
        """
        self.__signaling_device = _signaling_device

    #--------------------------------------------------------------------------------------

    def set_io_expander_int_callback_function(self, _callback) -> None:
        """!
        This will set a callback functions, which will be executed when the IO expander will generate an interrupt
        @param _callback: new callback function
        @return: None
        """
        self.__user_int_callback = _callback
    #--------------------------------------------------------------------------------------

    def __check_if_expander_io_is_available(self, _io_nr:int) -> bool:
        """!
        Checks if IO nr is available for the user (the 0-3 are reserved for power monitor!!)
        @param _io_nr: io nr
        @return: True is IO is available, False is not
        """

        if self.__expander is None:
            return False

        if _io_nr >= 4 and _io_nr <= 6:
            return True
        elif _io_nr > 6:
            print("IO pin does not exist: " + str(_io_nr))
            return False
        else:
            print("IO pin not available for user: " + str(_io_nr))
            return False

    #-------------------------------------------------------------------------------------

    def do_signaling_device(self) -> None:
        """!
        Will generated a system signal when possible
        @return: None
        """
        if self.__signaling_device is not None:
            self.__signaling_device.signal_system_alarm()
        else:
            print("No signaling device")

    #-------------------------------------------------------------------------------------

    def power_monitor_and_io_int_callback(self, _gpi_nr: int) -> None:
        """!
        The interrupt callback. Will be triggered by an interrupt generated by MCP23008
        Will check the io 0 un till 3 to detect the Power-fail of the DC/DC
        Also will go to the user callback

        Is called by ServoAssembly::__io_power_monitor_and_io_int_callback

        @param _gpi_nr (int) mr of the callback gpio pin
        @return None
        """

        interrupt_stats = self.__expander.read_interrupt_status()

        if RoboUtil.check_bit(interrupt_stats, 0) == 1:
            self.__timer0.start_checking_if_not_already_running()
        if RoboUtil.check_bit(interrupt_stats, 1) == 1:
            self.__timer1.start_checking_if_not_already_running()
        if RoboUtil.check_bit(interrupt_stats, 2) == 1:
            self.__timer2.start_checking_if_not_already_running()
        if RoboUtil.check_bit(interrupt_stats, 3) == 1:
            self.__timer3.start_checking_if_not_already_running()

        if self.__user_int_callback is not None:
            self.__user_int_callback(_gpi_nr)

    #--------------------------------------------------------------------------------------

    def power_monitor_and_io_int_reset_routine(self, _gpi_nr) -> None:
        """!
        This routine will be called to reset the interrupt handler of the MCP23008
        Is called by ServoAssembly::__io_power_monitor_and_io_int_reset_routine

        @param _gpi_nr: IO nr of the caller
        @return: None
        """

        timer = threading.Timer(1, self.__reset_timer_callback)
        timer.start()

    #-------------------------------------------------------------------------------------

    def __reset_timer_callback(self) -> None:
        """!
        function which will be executed after the int callback function is executed, to reset the interrupt routine
        @return: None
        """
        if self.__expander is None:
            return

        if self.disable_retry_timer_callback is True:
            return

        port_value = self.__expander.get_port_data() and 0x15       # only the first 4 bits are the interrupt for the power fail
        if port_value != 0x15:
            timer = threading.Timer(1, self.__reset_timer_callback)
            timer.start()
        else:
            if self.__expander is not None:
                self.__expander.reset_interrupts()

    #-------------------------------------------------------------------------------------







