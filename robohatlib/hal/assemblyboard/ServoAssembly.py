from __future__ import annotations

try:
    from robohatlib.hal.assemblyboard.servo.ServoBoard import ServoBoard
    from robohatlib.hal.assemblyboard.PowerMonitorAndIO import PowerMonitorAndIO
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib import Robohat_config
    from robohatlib.driver_ll.IOHandler import IOHandler
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
    from robohatlib.driver_ll.spi.SPIDeviceDef import SPIDeviceDef
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
except ImportError:
    print("Failed to resolve dependencies for ServoAssembly")
    raise



BASE_ADDRESS_MCP23008 = 0x20
BASE_ADDRESS_PCA9685 = 0x40

class ServoAssembly:

    def __init__(self, _io_handler: IOHandler, _servo_config: ServoAssemblyConfig, _i2c_bus_nr: int, _spi_bus_nr: int):
        """!
        @param _io_handler the IO handler, connection to all the IO
        @param _servo_config configuration of this ServoAssembly
        @param _i2c_bus_nr connected i2c bus nr
        @param _spi_bus_nr connected spi bus nr

        @return: none
        """

        self.__servo_config = _servo_config

        #----------------------------
        i2c_def_pwm = I2CDeviceDef("pwm_" + _servo_config.get_name(), _i2c_bus_nr, BASE_ADDRESS_PCA9685, _servo_config.get_sw1_pwm_address())
        if _io_handler.is_i2c_device_available is True:                     # check if the PWM controllers is present on the I2C bus.. if not.. no assemblyboard
            i2c_device_pwm = _io_handler.get_i2c_device(i2c_def_pwm)

            spi_def_adc = SPIDeviceDef("adc_" + _servo_config.get_name(), _spi_bus_nr, _servo_config.get_cs_adc_angle_readout())
            spi_device_adc = _io_handler.get_spi_device(spi_def_adc)

            if i2c_device_pwm is not None and spi_device_adc is not None:
                self.__servo_board = ServoBoard(i2c_device_pwm, spi_device_adc)

                servo_assembly_expander_def = Robohat_config.SERVOASSEMBLY_EXPANDER_DEF
                callbackholder = InterruptCallbackHolder("expander_callback_holder", self.__io_power_monitor_and_io_int_callback, self.__io_power_monitor_and_io_int_reset_routine, InterruptTypes.INT_FALLING, 250)
                servo_assembly_expander_def.set_callbackholder(callbackholder)

                self.__power_monitor_and_io = PowerMonitorAndIO(_io_handler, servo_assembly_expander_def, _servo_config.get_sw2_power_good_address(), _servo_config.get_name())
            else:
                self.__servo_board = None
        else:
            self.__servo_board = None

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def is_board_avaible(self) -> bool:
        """!
        Returns True when board is available
        @return: bool
        """
        if self.__servo_board is None:
            return False
        return True

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    def __io_power_monitor_and_io_int_callback(self, _gpio: int) -> None:
        """!
        Callback of interrupt service routine. This routine will be called when the IO expander interrupt fires
        @param _gpio: The GPIO nr which caused the interrupt. (Just for information purpose)
        @return: None
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.power_monitor_and_io_int_callback(_gpio)

    #--------------------------------------------------------------------------------------

    def __io_power_monitor_and_io_int_reset_routine(self, _gpio: int) -> None:
        """!
        Callback after the interrupt service routine is handled, to reset the interrupt and restart the check
        @param _gpio: The GPIO nr which caused the interrupt. (Just for information purpose)
        @return: None
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.power_monitor_and_io_int_reset_routine(_gpio)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def init_servo_assembly(self, _servo_datas_array: []) -> None:
        """!
        Initializes servo assembly

        @param _servo_datas_array:
        @return: none
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.init_power_monitor_and_io()

        if  self.__servo_board is not None:
            self.__servo_board.init_servo_board(_servo_datas_array)

    #--------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down
        @return: None
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.exit_program()

        if  self.__servo_board is not None:
            self.__servo_board.exit_program()
    #--------------------------------------------------------------------------------------

    def set_servo_single_angle(self, _servo_nr: int, _angle: float) -> None:
        """!
        Set the angle servo in degree

        @param _servo_nr The servo nr wanted (starts at 0)
        @param _angle wanted angle

        @return angle of connected servo in degree
        """
        if self.__servo_board is not None:
            self.__servo_board.set_servo_single_angle(_servo_nr, _angle)

    def get_servo_single_angle(self, _servo_nr: int) -> float:
        """!
        Get angle of connected servo in degree, or -1 when fails

        @param _servo_nr The servo nr wanted (starts at 0)
        @return angle of connected servo in degree, or 0 when not available
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_single_angle(_servo_nr)
        else:
            return -1

    # --------------------------------------------------------------------------------------

    def set_servo_multiple_angles(self, _wanted_angles: []) -> None:
        """!
        Set the angle of connected servos in degree

        @param _wanted_angles array of the angles

        @return angle of connected servo in degree
        """
        self.__servo_board.set_servo_multiple_angles(_wanted_angles)

    def get_all_servos_angle(self) -> []:
        """!
        @return angles of servos in degree
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_all_servos_angle()
        return []

    # --------------------------------------------------------------------------------------

    def get_servo_adc_readout_single_channel(self, _servo_nr: int) -> float:
        """!
        Get voltage of the potentiometer of the connected servo in vol

        @param _servo_nr The servo nr wanted (starts at 0)
        @return voltage of connected servo in volt or -1 when not available
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_readout_adc_single_channel(_servo_nr)
        return -1

    def get_adc_multiple_channels(self) -> []:
        """!
        @return voltages of the potentiometer of all the servos in volt
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_readout_adc_multiple_channels()
        return []

    # --------------------------------------------------------------------------------------
    def get_servo_is_connected(self, _servo_nr: int) -> bool:
        """!
        Checks if servo is connected. Returns False when not connected Servo starts at 0

        @param _servo_nr The servo nr
        @return Returns False when not connected
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_is_connected(_servo_nr)
        return False

    # --------------------------------------------------------------------------------------

    def sleep(self) -> None:
        """!
        Put the device into a sleep state

        @return None
        """
        self.__servo_board.sleep()

    # --------------------------------------------------------------------------------------

    def wake(self) -> None:
        """!
        Wake the device from its sleep state

        @return None
        """
        self.__servo_board.wake()

    # --------------------------------------------------------------------------------------

    def is_servo_sleeping(self) -> bool:
        """
        Get if Servos are sleeping
        @return (bool) returns True when servos are sleeping
        """
        return self.__servo_board.is_servo_sleeping()

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        return self.__servo_config.get_name()
    # --------------------------------------------------------------------------------------

    def get_sw1_pwm_address(self) -> int:
        return  self.__servo_config.get_sw1_pwm_address()

    # --------------------------------------------------------------------------------------

    def get_sw2_power_good_address(self) -> int:
        return self.__servo_config.get_sw2_power_good_address()

    # --------------------------------------------------------------------------------------

    def get_cs_adc_angle_readout(self) -> int:
        return self.__servo_config.get_cs_adc_angle_readout()

    # --------------------------------------------------------------------------------------

    def add_signaling_device(self, _signaling_device) -> None:
        """!
        Adds device which will alarms the user
        @param _signaling_device:
        @return: Nome
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.add_signaling_device(_signaling_device)

    # --------------------------------------------------------------------------------------
    def set_io_expander_direction(self, _io_nr: int, _direction: ExpanderDir) -> None:
        """!
        Set the direction of the IO pin

        @param _io_nr io nr
        @param _direction, 0 = Pin is configured as an output, 1 = Pin is configured as an input
        @return none
        """

        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.set_io_expander_direction(_io_nr, _direction)
    # --------------------------------------------------------------------------------------

    def get_io_expander_direction(self, _io_nr: int) -> ExpanderDir | None:
        """!
        get the direction of the IO pin

        @param _io_nr io nr
        @return ExpanderDir or none
        """
        if self.__power_monitor_and_io is not None:
            return self.__power_monitor_and_io.get_io_expander_direction(_io_nr)
        else:
            return None
    # --------------------------------------------------------------------------------------

    def set_io_expander_output(self, _io_nr: int, _value: ExpanderStatus) -> None:
        """!
        Set the output onto the desired value
        @param _io_nr: wanted io nr
        @param _value wanted value
        @return None
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.set_io_expander_output(_io_nr, _value)
    # --------------------------------------------------------------------------------------

    def get_io_expander_input(self, _pin_nr: int) -> ExpanderStatus | None:
        if self.__power_monitor_and_io is not None:
            return self.__power_monitor_and_io.get_io_expander_input(_pin_nr)
        else:
            return None

# --------------------------------------------------------------------------------------