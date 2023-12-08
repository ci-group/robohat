"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

from __future__ import annotations

try:
    from robohatlib.hal.assemblyboard.servo.ServoBoard import ServoBoard
    from robohatlib.hal.assemblyboard.PowerMonitorAndIO import PowerMonitorAndIO
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib import RobohatConfig
    from robohatlib.helpers.RoboUtil import RoboUtil
    from robohatlib.hal.assemblyboard.PwmPlug import PwmPlug
    from robohatlib.driver_ll.IOHandler import IOHandler
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import (
        InterruptCallbackHolder,
    )
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
    from robohatlib.driver_ll.spi.SPIDeviceDef import SPIDeviceDef
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.datastructs.IOStatus import IOStatus

except ImportError:
    print("Failed to resolve dependencies for ServoAssembly")
    raise


BASE_ADDRESS_MCP23008 = 0x20
BASE_ADDRESS_PCA9685 = 0x40


class ServoAssembly:
    def __init__(
        self,
        _io_handler: IOHandler,
        _servo_config: ServoAssemblyConfig,
        _i2c_bus_nr: int,
        _spi_bus_nr: int,
    ):
        """!
        @param _io_handler the IO handler, connection to all the IO
        @param _servo_config configuration of this ServoAssembly
        @param _i2c_bus_nr connected i2c bus nr
        @param _spi_bus_nr connected spi bus nr

        @return: none
        """

        self.__servo_config = _servo_config

        # ----------------------------
        i2c_def_pwm = I2CDeviceDef(
            "pwm_" + _servo_config.get_name(),
            _i2c_bus_nr,
            BASE_ADDRESS_PCA9685,
            _servo_config.get_sw1_pwm_address(),
        )
        if (
            _io_handler.is_i2c_device_detected(i2c_def_pwm) is True
        ):  # check if the PWM controllers is present on the I2C bus, if not, no assemblyboard
            print("Found: " + _servo_config.get_name())
            i2c_device_pwm = _io_handler.get_i2c_device(i2c_def_pwm)

            spi_cs: int = RoboUtil.get_pwm_cs_by_pwmplug(
                _servo_config.get_cs_adc_angle_readout()
            )

            spi_def_adc = SPIDeviceDef(
                "adc_" + _servo_config.get_name(), _spi_bus_nr, spi_cs
            )
            spi_device_adc = _io_handler.get_spi_device(spi_def_adc)

            if i2c_device_pwm is not None and spi_device_adc is not None:
                self.__servo_board = ServoBoard(
                    "servoboard_" + _servo_config.get_name(),
                    i2c_device_pwm,
                    spi_device_adc,
                )

                servo_assembly_expander_def = RobohatConfig.SERVOASSEMBLY_EXPANDER_DEF
                callbackholder = InterruptCallbackHolder(
                    "expander_callback_holder",
                    self.__io_power_monitor_and_io_int_callback,
                    self.__io_power_monitor_and_io_int_reset_routine,
                    InterruptTypes.INT_FALLING,
                    250,
                )
                servo_assembly_expander_def.set_callbackholder(callbackholder)

                self.__power_monitor_and_io = PowerMonitorAndIO(
                    _io_handler,
                    servo_assembly_expander_def,
                    _servo_config.get_sw2_power_good_address(),
                    _servo_config.get_name(),
                )
            else:
                self.__servo_board = None
        else:
            self.__servo_board = None

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def is_board_avaible(self) -> bool:
        """!
        Returns True when board is available
        @return: bool
        """
        if self.__servo_board is None:
            return False
        return True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def init_servo_assembly(self, _servo_datas_list: []) -> None:
        """!
        Initializes servo assembly

        @param _servo_datas_list:
        @return: none
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.init_io_expander()

        if self.__servo_board is not None:
            self.__servo_board.init_servo_board(_servo_datas_list)

    # --------------------------------------------------------------------------------------

    def servo_set_new_readout_vs_angle_formula(
        self, _servo_nr, _formula_a, _formula_b
    ) -> None:
        """!
        Set new formula parameters for voltage angle conversion
        @param _servo_nr: wanted servo nr
        @param _formula_a: first part of linear formula
        @param _formula_b: second part of linear formula
        @return: None
        """

        if self.__servo_board is not None:
            self.__servo_board.set_new_readout_vs_angle_formula(
                _servo_nr, _formula_a, _formula_b
            )

    # --------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down
        @return: None
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.exit_program()

        if self.__servo_board is not None:
            self.__servo_board.exit_program()

    # --------------------------------------------------------------------------------------

    def set_servo_direct_mode(self, _mode: bool, _delay: float = 0.0001) -> None:
        """!
        Sets if the servos are periodically updated, or direct
        @param _mode: True, direct mode activated
        @param _delay, delay in update mode is seconds
        @return: None
        """
        self.__servo_board.set_servo_direct_mode(_mode, _delay)

    # --------------------------------------------------------------------------------------

    def get_servo_is_direct_mode(self) -> bool:
        """!
        @return: if servo is NOT updated periodically
        """
        return self.__servo_board.get_servo_is_direct_mode()

    # --------------------------------------------------------------------------------------

    def get_servo_us_time(self, _degree: float, _servo_nr: int = 0) -> int:
        """!
        Get calculated time which is used to set the servo to the wanted degree
        @param _degree:
        @return: time in uS
        """

        return self.__servo_board.get_servo_us_time(_degree, _servo_nr)

    # --------------------------------------------------------------------------------------

    def get_servo_is_single_servo_wanted_angle(self, _servo_nr: int) -> bool:
        """!
        Returns true if (previous) wanted angle the same as the angle of the servo

        @param _servo_nr: The sero index
        @return: bool
        """

        return self.__servo_board.get_servo_is_single_servo_wanted_angle(_servo_nr)

    # --------------------------------------------------------------------------------------

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

        @param _wanted_angles list of the angles
        @return angle of connected servo in degree
        """
        self.__servo_board.set_servo_multiple_angles(_wanted_angles)

    # --------------------------------------------------------------------------------------

    def get_servo_multiple_angles(self) -> []:
        """!
        @return angles of servos in degree
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_multiple_angles()
        return []

    # --------------------------------------------------------------------------------------

    def get_servo_adc_single_channel(self, _servo_nr: int) -> float:
        """!
        Get voltage of the potentiometer of the connected servo in vol

        @param _servo_nr The servo nr wanted (starts at 0)
        @return voltage of connected servo in volt or -1 when not available
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_adc_single_channel(_servo_nr)
        return -1

    # --------------------------------------------------------------------------------------

    def get_servo_adc_multiple_channels(self) -> []:
        """!
        @return voltages of the angle of all the servos in volt. Returns a list of 16 elements
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_adc_multiple_channels()
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

    def set_update_value(self, _update_value: int) -> None:
        """!
        Set value which is used to add or subtract from current pos
        """
        if self.__servo_board is not None:
            self.__servo_board.set_update_value(_update_value)

    # --------------------------------------------------------------------------------------

    def put_to_sleep(self) -> None:
        """!
        Put the device into a sleep state

        @return None
        """
        if self.__servo_board is not None:
            self.__servo_board.put_to_sleep()

    # --------------------------------------------------------------------------------------

    def wake_up(self) -> None:
        """!
        Wake the device from its sleep state

        @return None
        """
        if self.__servo_board is not None:
            self.__servo_board.wake_up()

    # --------------------------------------------------------------------------------------

    def are_servos_sleeping(self) -> bool:
        """
        Get if Servos are sleeping
        @return (bool) returns True when servos are sleeping
        """
        if self.__servo_board is not None:
            return self.__servo_board.are_servos_sleeping()

        return True

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        return self.__servo_config.get_name()

    # --------------------------------------------------------------------------------------

    def get_sw1_pwm_address(self) -> int:
        return self.__servo_config.get_sw1_pwm_address()

    # --------------------------------------------------------------------------------------

    def get_sw2_power_good_address(self) -> int:
        return self.__servo_config.get_sw2_power_good_address()

    # --------------------------------------------------------------------------------------

    def get_cs_adc_angle_readout(self) -> PwmPlug:
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
    def set_servo_io_expander_direction(
        self, _io_nr: int, _direction: ExpanderDir
    ) -> IOStatus:
        """!
        Set the direction of the IO pin

        @param _io_nr io nr
        @param _direction, 0 = Pin is configured as an output, 1 = Pin is configured as an input
        @return none
        """

        if self.__power_monitor_and_io is not None:
            return self.__power_monitor_and_io.set_io_expander_direction(
                _io_nr, _direction
            )
        else:
            return IOStatus.IO_FAILED

    # --------------------------------------------------------------------------------------

    def get_servo_io_expander_direction(self, _io_nr: int) -> ExpanderDir:
        """!
        get the direction of the IO pin

        @param _io_nr io nr
        @return ExpanderDir or none
        """
        if self.__power_monitor_and_io is not None:
            return self.__power_monitor_and_io.get_io_expander_direction(_io_nr)
        else:
            return ExpanderDir.INVALID

    # --------------------------------------------------------------------------------------

    def set_servo_io_expander_output(
        self, _io_nr: int, _value: ExpanderStatus
    ) -> IOStatus:
        """!
        Set the output onto the desired value
        @param _io_nr: wanted io nr
        @param _value wanted value
        @return None
        """
        if self.__power_monitor_and_io is not None:
            return self.__power_monitor_and_io.set_io_expander_output(_io_nr, _value)
        else:
            return IOStatus.IO_FAILED

    # --------------------------------------------------------------------------------------

    def get_servo_io_expander_input(self, _pin_nr: int) -> ExpanderStatus:
        if self.__power_monitor_and_io is not None:
            return self.__power_monitor_and_io.get_io_expander_input(_pin_nr)
        else:
            return ExpanderStatus.INVALID

    # --------------------------------------------------------------------------------------

    def set_io_expander_int_callback_function(self, _callback) -> None:
        """!
        @param _callback:
        @return: None
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.set_io_expander_int_callback_function(_callback)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __io_power_monitor_and_io_int_callback(self, _gpio: int) -> None:
        """!
        Callback of interrupt service routine. This routine will be called when the IO expander interrupt fires
        @param _gpio: The GPIO nr which caused the interrupt. (Just for information purpose)
        @return: None
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.power_monitor_and_io_int_callback(_gpio)

    # --------------------------------------------------------------------------------------

    def __io_power_monitor_and_io_int_reset_routine(self, _gpio: int) -> None:
        """!
        Callback after the interrupt service routine is handled, to reset the interrupt and restart the check
        @param _gpio: The GPIO nr which caused the interrupt. (Just for information purpose)
        @return: None
        """
        if self.__power_monitor_and_io is not None:
            self.__power_monitor_and_io.power_monitor_and_io_int_reset_routine(_gpio)
