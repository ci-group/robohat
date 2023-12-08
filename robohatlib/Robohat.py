"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Main class
"""

from __future__ import annotations

try:
    from robohatlib import RobohatConfig
    from robohatlib import RobohatConstants
    from robohatlib.hal.assemblyboard.PwmPlug import PwmPlug

    from robohatlib.drivers.datastructs.McpInitStruct import McpInitStruct

    from robohatlib.driver_ll.IOHandler import IOHandler
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.constants.GpioDirection import GpioDirection
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder

    from robohatlib.hal.PowerManagement import PowerManagement
    from robohatlib.hal.Serial import Serial
    from robohatlib.hal.Buzzer import Buzzer
    from robohatlib.hal.LedMulticolor import LedMulticolor
    from robohatlib.hal.IMU import IMU
    from robohatlib.hal.IOExpander import IOExpander

    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.hal.datastructure.Color import Color
    from robohatlib.hal.datastructure.BatteryStatus import BatteryStatus

    from robohatlib.hal.assemblyboard.ServoAssembly import ServoAssembly
    from robohatlib.hal.TopboardADC import TopboardADC
    from robohatlib.hal.assemblyboard.servo.ServoBoard import ServoBoard
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData

    from robohatlib.driver_ll.datastructs.IOStatus import IOStatus

    from time import sleep
    from typing import Tuple

except ImportError:
    print("Failed to import needed dependencies for the Robohat class")
    raise

# --------------------------------------------------------------------------------------


class Robohat:
    """!
    Top class of Robohat library.
    The complete Robohat-hardware is only accessible by accessing this class. This is the connection between the user program and the hardware
    """
    __servo_assembly_1 = None
    __servo_assembly_2 = None
    __shadow_update_value = RobohatConfig.DEFAULT_DELAY_BETWEEN_ACTION
    # --------------------------------------------------------------------------------------
    # constructor Robohat

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __init__(self, _servo_assembly_1_config: ServoAssemblyConfig, _servo_assembly_2_config: ServoAssemblyConfig, _switch_top_board: int = 7):
        """!
        The Robohat base class initializer.

        Initializes all the IO
        Checks if the IO have no conflict (due wrong settings of the addresses)

        @param _servo_assembly_1_config config of servo assembly 1, see TestConfig.SERVOASSEMBLY_1_CONFIG as example
        @param _servo_assembly_2_config config of servo assembly 2, see TestConfig.SERVOASSEMBLY_2_CONFIG as example
        @param _switch_top_board dip-switch settings of the Topboard (board mounted on RPi), default 7. See the Hardware description for its address
        """

        print("\n")
        print("Starting Robohat lib: " + RobohatConstants.ROBOHAT_LIB_VERSION_STR + " (" + RobohatConstants.ROBOHAT_BUILD_DATE_STR + ") \n")

        if _servo_assembly_1_config is not None and _servo_assembly_2_config is not None:
            if _switch_top_board is _servo_assembly_1_config.get_sw2_power_good_address() or \
                    _switch_top_board is _servo_assembly_2_config.get_sw2_power_good_address() or \
                    _servo_assembly_1_config.get_sw2_power_good_address() is _servo_assembly_2_config.get_sw2_power_good_address():
                print("Error, dip-witches in config are in conflict, can't continue.")
                print("Preferred config is, the first assembly board on 0, the second assembly board on 1 and the switch onto the topboard on 7 ")
                return
        elif _servo_assembly_1_config is not None and _servo_assembly_2_config is None:
            if _switch_top_board is _servo_assembly_1_config.get_sw2_power_good_address():
                print("Error, dip-witches in config are in conflict, can't continue.")
                print("Preferred config is, the first assembly board on 0 and the switch onto the topboard on 7 ")
                return
        elif _servo_assembly_1_config is None and _servo_assembly_2_config is not None:
            if _switch_top_board is _servo_assembly_2_config.get_sw2_power_good_address():
                print("Error, dip-witches in config are in conflict, can't continue.")
                print("Preferred config is, the second assembly board on 1 and the switch onto the topboard on 7 ")
                return

        self.__io_handler = IOHandler()
        self.__serial = Serial(self.__io_handler, RobohatConfig.SERIAL_DEF)
        self.__buzzer = Buzzer(self.__io_handler, RobohatConfig.BUZZER_DEF)
        self.__led = LedMulticolor(self.__io_handler, RobohatConfig.STATUS_LED_DEF)
        self.__imu = IMU(self.__io_handler, RobohatConfig.IMU_DEF)

        #-------------------------------------Expander
        topboard_io_expander_def = RobohatConfig.TOPBOARD_IO_EXPANDER_DEF

        # at the default interrupt definition there are 2 callback added. the first for the trigger callback, the second for the interrupt reset callback
        topboard_io_expander_callbackholder = InterruptCallbackHolder("topboard_IO_expander_callback_holder",
                                                                 None, #self.__topboard_io_expander_int_callback,       # should be power-off pin, or the callback routine has to be set by the user. User can set it by 'InterruptCallbackHolder.set_callback_function' function if None
                                                                 self.__topboard_io_expander_int_reset_routine,
                                                                 InterruptTypes.INT_BOTH,
                                                                 250)

        topboard_io_expander_def.set_callbackholder(topboard_io_expander_callbackholder)

        self.__topboard_io_expander = IOExpander(self.__io_handler, topboard_io_expander_def, _switch_top_board)
        self.__topboard_adc = TopboardADC(self.__io_handler, RobohatConfig.TOPBOARD_ADC_I2C_DEF)

        self.__power_management = PowerManagement(self.__io_handler,
                                                  self.__topboard_adc,
                                                  RobohatConfig.POWER_SHUTDOWN_GPO_DEF)

        self.__power_management.add_signaling_device(self.__buzzer)

        if _servo_assembly_1_config is not None:
            self.__servo_assembly_1 = ServoAssembly(self.__io_handler,
                                                    _servo_assembly_1_config,
                                                    RobohatConfig.SERVOASSEMBLY_1_I2C_BUS,
                                                    RobohatConfig.SERVOASSEMBLY_1_SPI_BUS
                                                    )

            if self.__servo_assembly_1 .is_board_avaible() is True:
                self.__servo_assembly_1.add_signaling_device(self.__buzzer)
            else:
                self.__servo_assembly_1 = None              # if not available make None, so class is not accessible
        else:
            self.__servo_assembly_1 = None                  # if not available make None, so class is not accessible

# --------------------------------------------------------
        if _servo_assembly_2_config is not None:
            self.__servo_assembly_2 = ServoAssembly(self.__io_handler,
                                                    _servo_assembly_2_config,
                                                    RobohatConfig.SERVOASSEMBLY_2_I2C_BUS,
                                                    RobohatConfig.SERVOASSEMBLY_2_SPI_BUS
                                                    )

            if self.__servo_assembly_2.is_board_avaible() is True:
                self.__servo_assembly_2.add_signaling_device(self.__buzzer)
            else:
                self.__servo_assembly_2 = None              # if not available make None, so class is not accessible
        else:
            self.__servo_assembly_2 = None
# --------------------------------------------------------

        # Messages to the user
        if self.__servo_assembly_1 is None and self.__servo_assembly_2 is None:
            print("Error, no assembly-boards are available")
        elif self.__servo_assembly_1 is None:
            print("Warning, did not found assembly board 1")
        elif self.__servo_assembly_2 is None:
            print("Warning, did not found assembly board 2")

        self.set_update_value(RobohatConfig.DEFAULT_DELAY_BETWEEN_ACTION)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def init(self, _servo_board_1_datas_list: [], _servo_board_2_datas_list: []) -> None:
        """!
        Initializes the Robohat

        Mandatory. This function has to be called after creating the Robohat class

        @param _servo_board_1_datas_list, servo data list 1
        @param _servo_board_2_datas_list, servo data list 2

        @return None
        """

        self.__io_handler.init_io()
        self.__serial.init_serial()
        self.__buzzer.init_buzzer()
        self.__led.init_led()
        self.__imu.init_imu()

        self.__topboard_io_expander.init_io_expander()
        self.__topboard_adc.init_topboard_adc()
        self.__power_management.init_power_management()

        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.init_servo_assembly(_servo_board_1_datas_list)

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.init_servo_assembly(_servo_board_1_datas_list)

        self.__io_handler.start_interrupts()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """!
        Exit the program. Will shut down all the software processes and the hardware
        Should be used when exiting your application
        @return: None
        """
        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.exit_program()

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.exit_program()

        self.__serial.exit_program()
        self.__imu.exit_program()
        self.__topboard_io_expander.exit_program()
        self.__topboard_adc.exit_program()

        self.__led.exit_program()
        self.__buzzer.exit_program()
        self.__power_management.exit_program(False)

        self.__io_handler.exit_program()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # begin I2C functions ---------------------------------------------------------------------------------
    def do_i2c_scan(self) -> None:
        """!
        Scans all the available I2C busses on the Robohat hardware
        Displays the found I2C devices onto the console
        @return None
        """

        self.__io_handler.do_i2c_scan()

    # end I2C functions ---------------------------------------------------------------------------------
    # begin BUZZER functions -----------------------------------------------------------------------------
    def do_buzzer_random(self) -> None:
        """!
        Generates a random sound

        @return None
        """
        self.__buzzer.buzzer_random()

    def do_buzzer_slowwoop(self) -> None:
        """!
        Generates a sound from 2000Hz to 50Hz

        @return None
        """

        self.__buzzer.buzzer_slowwoop()

    def do_buzzer_beep(self) -> None:
        """!
        Short beep of the buzzer

        @return None
        """
        self.__buzzer.buzzer_beep()

    def do_buzzer_freq(self, _freq: int) -> None:
        """!
         Beeps the buzzer at a requested frequency

         @param _freq wanted frequency in Hz
         @return None
         """
        self.__buzzer.buzzer_freq(_freq)

    def do_buzzer_release(self) -> None:
        """!
        Stops the buzzer from making sound
        @return: None
        """
        self.__buzzer.buzzer_release()
    # end BUZZER functions ------------------------------------------------------------------------------------

    # begin LED functions ---------------------------------------------------------------------------------
    def set_led_color(self, _color: Color) -> None:
        """!
         Sets the color of the LED and turns the LED on
         Valid colors are: WHITE, RED, GREEN, BLUE, YELLOW, and PURPLE

         @param _color waned color
         @return None
         """
        self.__led.set_led_color(_color)

    def turn_led_off(self) -> None:
        """!
         Turns led off, last color will be stored

         @return None
         """
        self.__led.turn_led_off()

    def turn_led_on(self) -> None:
        """!
        Turns led on, with last known color. default color is WHITE

        @return None
        """
        self.__led.turn_led_on()

    def get_led_color(self) -> Color:
        """!
        Get current color of the LED

        @return: Color
        """
        return self.__led.get_led_color()

    # end LED functions ------------------------------------------------------------------------------------

    # begin Servo functions --------------------------------------------------------------------------------------
    def do_servo_fit_formula_readout_vs_angle_single_servo(self, _servo_nr: int) -> None:
        """!
        Set new formula parameters for voltage angle conversion by setting the servo at angle of 20 and 160
        and readout the voltage of the ADC
        @param _servo_nr: wanted servo nr
        @return: None
        """

        if self.get_servo_is_connected(_servo_nr) is False:
            print("Sorry, but servo  " + str(_servo_nr) + " is not connected")
            return

        print("Going to fit voltage to angle for Servo " + str(_servo_nr))

        value_y1 = 20.0
        value_y2 = 160.0
        self.set_servo_single_angle(_servo_nr, value_y1)
        sleep(2)
        value_x1 = self.get_servo_adc_single_channel(_servo_nr)
        sleep(0.1)
        self.set_servo_single_angle(_servo_nr, value_y2)
        sleep(2)
        value_x2 = self.get_servo_adc_single_channel(_servo_nr)

        a = (value_y2 - value_y1) / (value_x2 - value_x1)
        b = value_y1 - (a * value_x1)

        print("Formula is: " + str(a) + "x + " + str(b) + " created out of: (" + str(value_x1) + "," + str(value_y1) + "),(" + str(value_x2) + "," + str(value_y2) + ")")
        self.servo_set_new_readout_vs_angle_formula(_servo_nr, a, b)

#----------------------

    def do_servo_fit_formula_readout_vs_angle_multiple_servos(self, _min_range, _max_range) -> None:
        """!
        Set new formula parameters for voltage angle conversion by setting the servo at angle of 20 and 160
        and readout the voltage of the ADC
        @param _min_range: ange minial
        @param _max_range: angle maximal
        @return: None
        """

        avail_servos = self.__get_servos_start_stop_depending_available_assembly_board()
        first_servo = avail_servos[0]
        last_servo = avail_servos[1]

        pre_angles = self.get_servo_multiple_angles()
        previous_direct_mode:bool = self.get_servo_is_direct_mode()

        self.set_servo_direct_mode(False)

        print("Setting servos to min: " + str(_min_range) + "°" )
        self.set_servo_multiple_angles(
            [
                _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range,
                _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range, _min_range
            ])

        self.do_wait_until_servos_are_wanted_angles(first_servo, last_servo, 15)
        sleep(2)

        voltages_min = self.get_servo_adc_multiple_channels()
        sleep(0.1)
        print("Setting servos to max: " + str(_max_range) + "°")
        self.set_servo_multiple_angles(
            [
                _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range,
                _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range, _max_range
            ])

        self.do_wait_until_servos_are_wanted_angles(first_servo, last_servo, 15)
        sleep(2)

        voltage_max = self.get_servo_adc_multiple_channels()
        sleep(0.1)

        for servo_nr in range(0, len(pre_angles)):
            pos = pre_angles[servo_nr]
            if pos != -1:
                voltage_range_servo = voltage_max[servo_nr] - voltages_min[servo_nr]

                if voltage_range_servo != 0:
                    a = (_max_range - _min_range) / voltage_range_servo
                    b = _min_range - (a * voltages_min[servo_nr])
                    print("Servo: " + str(servo_nr) + " formula is: " + str(a) + "x + " + str(b) + " created out of: (" + str(voltages_min[servo_nr]) + "," + str(_min_range) + "),(" + str(voltage_max[servo_nr]) + "," + str(_max_range) + ")")
                    self.servo_set_new_readout_vs_angle_formula(servo_nr, a, b)
                else:
                    print("Voltage range is 0, divide by zero")

        self.do_wait_until_servos_are_wanted_angles(first_servo, last_servo, 15)
        sleep(2)

        default_degree = 90
        print("Setting all servos to " + str(default_degree) + " °")
        self.set_servo_multiple_angles(
            [
                default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree,
                default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree, default_degree
            ])

        self.do_wait_until_servos_are_wanted_angles(first_servo, last_servo, 15)
        sleep(2)
        self.set_servo_direct_mode(previous_direct_mode)

    # ----------------------------------

    def set_servo_direct_mode(self, _mode:bool, _delay:float = 0.0001) -> None:
        """!
        Sets if the servos are periodically updated, or direct
        @param _mode: True, direct mode activated
        @param _delay, delay in update mode is seconds
        @return: None
        """
        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.set_servo_direct_mode(_mode, _delay)
        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.set_servo_direct_mode(_mode, _delay)
    # ----------------------------------

    def get_servo_is_direct_mode(self) -> bool:
        """!
        @return: if servo is NOT updated periodically
        """
        if self.__servo_assembly_1 is not None:
            return self.__servo_assembly_1.get_servo_is_direct_mode()
        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.get_servo_is_direct_mode()

        return True

#----------------------------------

    def servo_set_new_readout_vs_angle_formula(self, _servo_nr, _formula_a, _formula_b) -> None:
        """!
        Set new formula parameters for voltage angle conversion
        @param _servo_nr: wanted servo nr
        @param _formula_a: first part of linear formula
        @param _formula_b: second part of linear formula
        @return: None
        """

        assemble_board = self.__get_servo_assembly_depending_servo_nr(_servo_nr)
        if assemble_board is not None:
            servo_nr = self.__get_servo_nr_depending_assembly(_servo_nr)
            assemble_board.servo_set_new_readout_vs_angle_formula(servo_nr, _formula_a, _formula_b)

    # ----------------------------------

    def get_servo_is_connected(self, _servo_nr: int) -> bool:
        """!
        Checks if servo is connected. Returns False when not connected.
        Servos 0 - 15 are connected to assembly board 0 (PWMPLUG 3) and servos 15 - 31 are connected to assembly
        board 1 (PWMPLUG 4)

        @param _servo_nr The servo nr 0 - 31
        @return: Returns False when not connected
        """
        if _servo_nr >= 0 or _servo_nr < 16:
            if self.__servo_assembly_1 is None:
                return False

            servo_nr = self.__get_servo_nr_depending_assembly(_servo_nr)
            if servo_nr is not None:
                return self.__servo_assembly_1.get_servo_is_connected(servo_nr)
            return False

        elif _servo_nr >= 16 or _servo_nr < 32:
            if self.__servo_assembly_2 is None:
                return False

            servo_nr = self.__get_servo_nr_depending_assembly(_servo_nr)
            if servo_nr is not None:
                return self.__servo_assembly_2.get_servo_is_connected(servo_nr)
            return False
        else:
            return False

    # --------------------------------------------------------------------------------------
    def get_assemblyboard_is_connected(self, _board_id: PwmPlug) -> bool:
        """!
        Check is an assemblyboard is available. Returns true when available
        @param _board_id: id of requested assemblyboard. Use Robohat_constants.PWMPLUG_P3 or Robohat_constants.PWMPLUG_P4
        @return: bool
        """

        if _board_id is PwmPlug.PWMPLUG_P3:
            if self.__servo_assembly_1 is not None:
                return True
        elif _board_id is PwmPlug.PWMPLUG_P4:
            if self.__servo_assembly_2 is not None:
                return True
        return False

    # ----------------------------------

    def get_servo_is_single_servo_wanted_angle(self, _servo_nr: int) -> bool:
        """!
        Returns true if (previous) wanted angle is the same as the current angle of the servo

        @param _servo_nr: The wanted servo id
        @return: bool
        """

        servo_assembly = self.__get_servo_assembly_depending_servo_nr(_servo_nr)    # the assembly depending on servo_nr
        if servo_assembly is not None:
            servo_nr = self.__get_servo_nr_depending_assembly(_servo_nr)            # servo nr of the servo of the assembly
            if servo_nr is not None:
                return servo_assembly.get_servo_is_single_servo_wanted_angle(servo_nr)

        return False

    # ----------------------------------

    def do_wait_until_servo_is_wanted_angle(self, _servo_nr: int, _time_in_seconds_until_escape=15):
        """!
        Wait until current angles are the same as the wanted angles

        @param _servo_nr:The wanted servo id
        @param _time_in_seconds_until_escape: Time to prevent endless loop
        @return: None
        """
        counter_seconds = 0
        counter_100ms = 0

        while self.get_servo_is_single_servo_wanted_angle(_servo_nr) is False:
            sleep(0.1)
            counter_100ms = counter_100ms + 1
            if counter_100ms == 10:
                counter_seconds = counter_seconds + 1
                counter_100ms = 0

            if counter_seconds >= _time_in_seconds_until_escape:
                break
    # --------------------------------------------------------------------------------------

    def get_servo_are_multiple_servos_wanted_angles(self, _first_servo: int, _last_servo: int) -> bool:
        """!
        Returns true if (previous) wanted angles are the same as the actual angles of the servos

        @param _first_servo: The first servo of the pool of servos
        @param _last_servo: The last servo of the pool of servos
        @return: bool
        """

        return_value:bool = True

        for servo_nr in range(_first_servo, (_last_servo + 1)):
            return_value = return_value and self.get_servo_is_single_servo_wanted_angle(servo_nr)

        return return_value

    # --------------------------------------------------------------------------------------

    def do_wait_until_servos_are_wanted_angles(self, _first_servo: int, _last_servo: int, _time_in_seconds_until_escape = 15):
        """!
        Wait until current angles are the same as the wanted angles

        @param _first_servo: The first servo of the pool of servos
        @param _last_servo: The last servo of the pool of servos
        @param _time_in_seconds_until_escape: Maximum time before ending the wait loop, to prevent endless loop. Default 15 seconds
        @return: None
        """
        counter_seconds = 0
        counter_100ms = 0

        while self.get_servo_are_multiple_servos_wanted_angles(_first_servo, _last_servo) is False:
            sleep(0.1)
            counter_100ms = counter_100ms + 1
            if counter_100ms == 10:
                counter_seconds = counter_seconds + 1
                counter_100ms = 0

            if counter_seconds >= _time_in_seconds_until_escape:
                break

    # --------------------------------------------------------------------------------------

    def get_servo_adc_single_channel(self, _servo_nr: int) -> float:
        """!
        Get angle of connected servo in degree or -1 when an error occurs
        Servos 0 - 15 are connected to assembly board 0 (PWMPLUG 3) and servos 15 - 31 are connected to assembly
        board 1 (PWMPLUG 4)

        @param _servo_nr The servo nr wanted, the servo nr 0 - 31
        @return angle or -1
        """

        servo_assembly = self.__get_servo_assembly_depending_servo_nr(_servo_nr)    # the assembly depending on servo_nr
        if servo_assembly is not None:
            servo_nr = self.__get_servo_nr_depending_assembly(_servo_nr)            # servo nr of the servo of the assembly
            if servo_nr is not None:
                return servo_assembly.get_servo_adc_single_channel(servo_nr)
        return -1

    # --------------------------------------------------------------------------------------

    def get_servo_adc_multiple_channels(self) -> []:
        """!
        Get voltages of the angle of all the servos. The list consists of 32 elements.
        @return a list of voltages
        """

        return_data = [-1.0] * 32

        if self.__servo_assembly_1 is not None:
            data_assembly1 = self.__servo_assembly_1.get_servo_adc_multiple_channels()
            for i in range(0, 16):
                return_data[i] = data_assembly1[i]

        if self.__servo_assembly_2 is not None:
            data_assembly2 = self.__servo_assembly_2.get_servo_adc_multiple_channels()
            for i in range(0, 16):
                return_data[i+ 16] = data_assembly2[i]

        if self.__servo_assembly_1 is None and self.__servo_assembly_2 is None:
            print("Error, no assemblies found, requesting ADC data")

        return return_data
    # --------------------------------------------------------------------------------------

    def get_servo_single_angle(self, _servo_nr: int) -> float:
        """!
        Get angle of connected servo in degree or -1 when an error occurs
        Servos 0 - 15 are connected to assembly board 0 (PWMPLUG 3) and servos 15 - 31 are connected to assembly
        board 1 (PWMPLUG 4)

        @param _servo_nr The servo nr wanted (0 - 31)
        @return angle or -1
        """

        servo_assembly = self.__get_servo_assembly_depending_servo_nr(_servo_nr)  # the assembly depending on servo_nr
        if servo_assembly is not None:
            servo_nr = self.__get_servo_nr_depending_assembly(_servo_nr)  # servo nr of the servo of the assembly
            if servo_nr is not None:
                return servo_assembly.get_servo_single_angle(servo_nr)
        return -1
    # --------------------------------------------------------------------------------------

    def set_servo_single_angle(self, _servo_nr: int, _angle: float) -> None:
        """!
        Set the angle of connected servo in degree, does nothing when not avaible
        Servos 0 - 15 are connected to assembly board 0 (PWMPLUG 3) and servos 15 - 31 are connected to assembly
        board 1 (PWMPLUG 4)

        @param _servo_nr The servo nr wanted (0 - 31)
        @param _angle wanted angle

        @return None
        """
        servo_assembly = self.__get_servo_assembly_depending_servo_nr(_servo_nr)
        if servo_assembly is not None:
            servo_nr = self.__get_servo_nr_depending_assembly(_servo_nr)
            if servo_nr is not None:
                servo_assembly.set_servo_single_angle(servo_nr, _angle)
            elif RobohatConfig.DEBUG is True:
                print("Unknown servo")
        elif RobohatConfig.DEBUG is True:
            print("Did not found servo assembly")


    # ------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------

    def get_servo_multiple_angles(self) -> []:
        """!
        Get a list of the angles of all the servos
        a list of 32 elements will be returned

        @return angles list
        """

        return_data = [-1.0] * 32

        if self.__servo_assembly_1 is not None:
            data_assembly1 = self.__servo_assembly_1.get_servo_multiple_angles()
            for i in range(0, 16):
                return_data[i] = data_assembly1[i]

        if self.__servo_assembly_2 is not None:
            data_assembly2 = self.__servo_assembly_2.get_servo_multiple_angles()
            for i in range(0, 16):
                return_data[i+16] = data_assembly2[i]

        return return_data

    # ------------------------------------------------------------------------------------------

    def get_servo_us_time(self, _degree:float, _servo_nr:int=0) -> int:
        """!
        Get calculated time which is used to set the servo to the wanted degree
        @param _degree: wanted angle
        @param _servo_nr the wanted servo
        @return: time in uS
        """

        if self.__servo_assembly_1 is not None:
            return self.__servo_assembly_1.get_servo_us_time(_degree, _servo_nr)
        elif self.__servo_assembly_2 is not None:
            return self.__servo_assembly_2.get_servo_us_time(_degree, _servo_nr)
        else:
            return 0

    # ------------------------------------------------------------------------------------------

    def set_servo_multiple_angles(self, _angles_list: []) -> None:
        """!
        Set the angle of connected servos in degree
        Expect a list of angles. The list should have 16 elements (if only assembly 1 is connected) or list should
        have 32 elements (if both assemblies are connected)

        @param _angles_list, list of the angles
        @return None
        """

        # if Robohat_config.DEBUG is True:
        #     print(_angles_list)

        if self.__servo_assembly_1 is not None and len(_angles_list) >= 16:
            angles_list1 = [0.0] * 16
            for i in range(0, 16):
                angles_list1[i] = _angles_list[i]
            self.__servo_assembly_1.set_servo_multiple_angles(angles_list1)

        if self.__servo_assembly_2 is not None and len(_angles_list) >= 32:
            angles_list2 = [0.0] * 16
            for i in range(0, 16):
                angles_list2[i] = _angles_list[i + 16]
            self.__servo_assembly_2.set_servo_multiple_angles(angles_list2)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_update_value(self, _update_value: int) -> None:
        """!
        Set value which is used to add or subtract from current pos
        """
        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.set_update_value(_update_value)
        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.set_update_value(_update_value)
        self.__shadow_update_value = _update_value

    # --------------------------------------------------------------------------------------

    def get_update_value(self) -> int:
        """!
        get value which is used to add or subtract from current pos
        """
        return self.__shadow_update_value

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def put_servo_to_sleep(self) -> None:
        """!
        Puts servos to sleep. Note servos will be powered down
        @return: None
        """

        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.put_to_sleep()

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.put_to_sleep()

    # ------------------------------------------------------------------------------------------

    def wakeup_servo(self) -> None:
        """!
        Wakes up the servos
        @return: None
        """

        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.wake_up()

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.wake_up()

    # ------------------------------------------------------------------------------------------

    def are_servos_sleeping(self) -> bool:
        """
        Get if Servos are sleeping
        @return: True when servos are sleeping
        """

        if self.__servo_assembly_1 is not None:
            return self.__servo_assembly_1.are_servos_sleeping()

        elif self.__servo_assembly_2 is not None:
            return self.__servo_assembly_2.are_servos_sleeping()

        return True


    # ------------------------------------------------------------------------------------------

    def set_servo_io_expander_direction(self, _board_id: PwmPlug, _pin_nr: int, _dir: ExpanderDir) -> IOStatus:
        """!
        Set the direction of the IO pin on a servo board.
        @param _board_id: board nr
        @param _pin_nr:  pin nr
        @param _dir: on or out
        @return None:
        """

        if _board_id is PwmPlug.PWMPLUG_P3:               # board 0
            if self.__servo_assembly_1 is not None:
                return self.__servo_assembly_1.set_servo_io_expander_direction(_pin_nr, _dir)
            else:
                print("Error: servo assembly 1 not initialized")
                return IOStatus.IO_FAILED
        elif _board_id is PwmPlug.PWMPLUG_P4:             # board 1
            if self.__servo_assembly_2 is not None:
                return self.__servo_assembly_2.set_servo_io_expander_direction(_pin_nr, _dir)
            else:
                print("Error: servo assembly 2 not initialized")
                return IOStatus.IO_FAILED
        else:
            print("Board nr not available")
            return IOStatus.IO_FAILED

    # ------------------------------------------------------------------------------------------

    def get_servo_io_expander_direction(self, _board_id: PwmPlug, _pin_nr: int) -> ExpanderDir:
        """!
        Set the direction of the IO pin on a servo board.
        @param _board_id: id of requested assemblyboard
        @param _pin_nr:  pin nr
        @return ExpanderDir:
        """

        if _board_id == PwmPlug.PWMPLUG_P3:               # board 0
            if self.__servo_assembly_1 is not None:
                return self.__servo_assembly_1.get_servo_io_expander_direction(_pin_nr)
            else:
                print("Error: servo assembly 1 not initialized")
                return ExpanderDir.INVALID
        elif _board_id == PwmPlug.PWMPLUG_P4:             # board 1
            if self.__servo_assembly_2 is not None:
                return self.__servo_assembly_2.get_servo_io_expander_direction(_pin_nr)
            else:
                print("Error: servo assembly 2 not initialized")
                return ExpanderDir.INVALID
        else:
            print("Board nr not available")
        return ExpanderDir.INVALID

    # ------------------------------------------------------------------------------------------

    def set_servo_io_expander_output(self, _board_id: PwmPlug, _pin_nr: int, _value: ExpanderStatus) -> IOStatus:
        """!
        Set the value of the IO pin on a servo board. Note, io pin should be an output
        @param _board_id: id of requested assemblyboard
        @param _pin_nr:  pin nr
        @param _value: low or high
        @return None:
        """
        if _board_id == PwmPlug.PWMPLUG_P3:               # board 0
            if self.__servo_assembly_1 is not None:
                return self.__servo_assembly_1.set_servo_io_expander_output(_pin_nr, _value)
            else:
                print("Error: servo assembly 1 not initialized")
                return IOStatus.IO_FAILED
        elif _board_id == PwmPlug.PWMPLUG_P4:             # board 1
            if self.__servo_assembly_2 is not None:
                return self.__servo_assembly_2.set_servo_io_expander_output(_pin_nr, _value)
            else:
                print("Error: servo assembly 2 not initialized")
                return IOStatus.IO_FAILED
        else:
            print("Board nr not available")
            return IOStatus.IO_FAILED
    # ------------------------------------------------------------------------------------------

    def get_servo_io_expander_input(self, _board_id: PwmPlug, _pin_nr: int) -> ExpanderStatus:
        """!
        Get the value of the IO pin on a servo board. Note, io pin should be an output
        @param _board_id: board nr
        @param _pin_nr:  pin nr
        @return None:
        """
        if _board_id == PwmPlug.PWMPLUG_P3:               # board 0
            if self.__servo_assembly_1 is not None:
                return self.__servo_assembly_1.get_servo_io_expander_input(_pin_nr)
            else:
                print("Error: servo assembly 1 not initialized")
                return ExpanderStatus.INVALID
        elif _board_id == PwmPlug.PWMPLUG_P4:             # board 1
            if self.__servo_assembly_2 is not None:
                return self.__servo_assembly_2.get_servo_io_expander_input(_pin_nr)
            else:
                print("Error: servo assembly 2 not initialized")
                return ExpanderStatus.INVALID
        else:
            print("Board nr not available")
        return ExpanderStatus.INVALID

    # -----------------------------------------------------------------------------------------
    # noinspection PyMethodMayBeStatic
    def __get_servo_nr_depending_assembly(self, _servo_nr: int) -> int | None:
        """!
        Get the servo nr of the assembly (so servo nr 16 will be servo nr 0 of assembly 2). If not available
        None will be returned

        @param _servo_nr The servo nr wanted (starts at 0)
        @return servo number or None
        """

        if _servo_nr >= 0 and _servo_nr < 16:
            return _servo_nr
        elif _servo_nr >= 16 and _servo_nr < 32:
            return _servo_nr - 16
        else:
            print("Error: requested " + str(_servo_nr) + " is not available")
            return None

    # ------------------------------------------------------------------------------------------

    def __get_servo_assembly_depending_servo_nr(self, _servo_nr: int) -> ServoAssembly | None:
        """!
        Get servo_assembly depending on servo nr or None when an error occurs

        @param _servo_nr The servo nr wanted (starts at 0)
        @return servo_nr or None
        """

        if _servo_nr >= 0 and _servo_nr < 16:
            if self.__servo_assembly_1 is None:
                print("Error: servo assembly 1 not initialized")
                return None
            return self.__servo_assembly_1

        elif _servo_nr >= 16 and _servo_nr < 32:
            if self.__servo_assembly_2 is None:
                print("Error: servo assembly 2 not initialized")
                return None
            return self.__servo_assembly_2
        else:
            print("Error: requested servo " + str(_servo_nr) + " is not available")
            return None

    # end Servo functions --------------------------------------------------------------------------------------

    # begin Topboard ADC functions --------------------------------------------------------------------------------------
    def get_topboard_adc_single_channel(self, _channel_nr: int) -> float:
        """!
        Get analog value of a channel from the Topboard adc
        Requested channels can be 0 - 3 (channel 3 is the derivative of the battery voltage)

        @param _channel_nr Wanted channel nr. (Starts at 0)
        @return analog voltage
        """

        return self.__topboard_adc.get_adc_single_channel(_channel_nr)

    # ------------------------------------------------------------------------------------------

    def get_topboard_adc_multiple_channels(self) -> []:
        """!
        Get analog values of the HAT adc
        Returns a list of 4 elements

        @return analog voltage in a list
        """
        return self.__topboard_adc.get_adc_multiple_channels()

    # end Topboard ADC functions --------------------------------------------------------------------------------------

    # begin Topboard IO_EXPANDER functions ---------------------------------------------------------------------------------
    def set_topboard_io_expander_direction(self, _io_nr:int, _direction: ExpanderDir) -> IOStatus:
        """!
        Set the direction of an io pin of the IO expander

        @param _io_nr io nr
        @param _direction the direction of the pin.

        @return IOStatus
        """

        return self.__topboard_io_expander.set_io_expander_direction(_io_nr, _direction)

    def get_topboard_io_expander_direction(self, _io_nr:int) -> ExpanderDir:
        """!
        Get the direction of an io pin of the IO expander

        @param _io_nr io nr

        @return ExpanderDir
        """

        return self.__topboard_io_expander.get_io_expander_direction(_io_nr)

    def set_topboard_io_expander_output(self, _io_nr: int, _status: ExpanderStatus) -> IOStatus:
        """!
        Set the output status of an io pin of the IO expander

        Note. direction of the pin must be an Output

        @param _io_nr io nr
        @param _status the status o the pin

        @return None
        """
        return self.__topboard_io_expander.set_io_expander_output(_io_nr, _status)

    def get_topboard_io_expander_input(self, _io_nr: int) -> ExpanderStatus:
        """!
        get the input status of an io pin of the IO expander
        Note. direction of the pin must be an Input

        @param _io_nr io nr
        @return ExpanderStatus
        """
        return self.__topboard_io_expander.get_io_expander_input(_io_nr)

    def set_topboard_io_expander_int_callback(self, _callback) -> None:
        """!
        Set a new function which will be executed when the topboard-io-expander is triggerd
        @param _callback: the callback function
        @return: None
        """
        if self.__topboard_io_expander is not None:
            self.__topboard_io_expander.set_io_expander_int_callback_function(_callback)

    def set_topboard_io_expander_int_release_function(self, _callback) -> None:
        """!
        Set a new function which will be executed after the interrupt callback function is executed
        @param _callback: the callback function
        @return: None
        """
        if self.__topboard_io_expander is not None:
            self.__topboard_io_expander.set_io_expander_int_release_function(_callback)

    def __topboard_io_expander_int_reset_routine(self, _gpi_nr: int) -> None:
        """!
        This routine will be called to reset the interrupt handler (if needed, is used by MCP23008)
        @param _gpi_nr: IO nr of the caller
        @return: None
        """
        if self.__topboard_io_expander is not None:
            self.__topboard_io_expander.reset_interrupt(_gpi_nr)

    # end Topboard IO_EXPANDER functions ------------------------------------------------------------------------------------

    # begin IMU functions ---------------------------------------------------------------------------------
    def get_imu_magnetic_fields(self) -> Tuple[float, float, float] | None:
        """!
        Get the magnetic fields

        @return a tuple of the magnetic fields values x,y,z or None when not available
        """
        return self.__imu.get_magnetic_fields()

    def get_imu_acceleration(self) -> Tuple[float, float, float] | None:
        """!
        Get the acceleration of the Robohat

        @return a tuple of the guro values x,y,z or None when not available
        """
        return self.__imu.get_acceleration()

    def get_imu_gyro(self) -> Tuple[float, float, float] | None:
        """!
        Get the values of the Gyro

        @return a tuple of the guro values x,y,z or None when not available
        """
        return self.__imu.get_gyro()

    def do_imu_test(self) -> None:
        """!
        Just a IMU test

        @return None
        """
        self.__imu.do_imu_test()


    # end IMU functions ------------------------------------------------------------------------------------
    # begin Power management functions ---------------------------------------------------------------------
    def get_battery_percentage_capacity(self) -> int:
        """!
        Get capacity of battery in percentage

        @return: percentage of the battery
        """
        return self.__power_management.get_battery_percentage_capacity()

    def get_battery_voltage(self) -> float:
        """!
        Get voltage of battery

        @return: voltage of battery
        """

        return self.__power_management.get_battery_voltage()

    def get_battery_status(self) -> BatteryStatus:
        """!
        Returns True if battery capacity is OK

        @return True is battery capacity is OK
        """
        return self.__power_management.get_battery_status()

    # end Power management functions -------------------------------------------------------------------------
    # begin System functions ---------------------------------------------------------------------------------

    def do_system_shutdown(self) -> None:
        """!
        Sends shutdown signal to power module, cleans-up IO, shutdowns the RPi
        @return None
        """

        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.exit_program()

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.exit_program()

        self.__serial.exit_program()
        self.__imu.exit_program()
        self.__topboard_io_expander.exit_program()
        self.__topboard_adc.exit_program()

        self.__led.exit_program()
        self.__buzzer.exit_program()

        self.__power_management.shutdown_power()

    # ------------------------------------------------------------------------------------
    def set_system_alarm_permitted(self, _state: bool) -> None:
        """!
        Overrides the system alarm switch. If false, no sound alarm will be given
        @param _state: new state of system alarm
        @return: None
        """
        self.__buzzer.set_status_system_alarm_permitted(_state)

    # ------------------------------------------------------------------------------------
    def get_system_alarm_permitted(self) -> bool:
        """!
        Get the system alarm switch. If false, no sound alarm will be given
        @return: None
        """
        return self.__buzzer.get_status_system_alarm_permitted()

    # end System management functions -------------------------------------------------------------------------

    # begin Library functions ---------------------------------------------------------------------------------
    # noinspection PyMethodMayBeStatic
    def get_lib_version(self) -> str:
        """!
        Get version number of library.

        @return str, version number of library, such as 1.0.1
        """

        return RobohatConstants.ROBOHAT_LIB_VERSION_STR

    # ------------------------------------------------------------------------------------
    # noinspection PyMethodMayBeStatic
    def get_lib_build_date(self) -> str:
        """!
        Get the build date of library.

        @return str, version build date of library, such as 20231225
        """
        return RobohatConstants.ROBOHAT_BUILD_DATE_STR

    # End Library functions ---------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------
    def get_buzzer(self) -> Buzzer:
        """!
        Return the buzzer device for signaling purposes
        @return Buzzer device
        """
        return self.__buzzer

    # ------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------

    def set_assemblyboard_1_io_expander_int_callback(self, _callback) -> None:
        """!
        Set a (new) function which will be executed when the io-expander of the assembly board 1 is triggerd
        @param _callback: callback function
        @return: None
        """
        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.set_io_expander_int_callback_function(_callback)

    def set_assemblyboard_2_io_expander_int_callback(self, _callback) -> None:
        """!
        Set a (new) function which will be executed when the io-expander of the assembly board 2 is triggerd
        @param _callback: callback function
        @return: None
        """
        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.set_io_expander_int_callback_function(_callback)

    # ------------------------------------------------------------------------------------

    def __get_servos_start_stop_depending_available_assembly_board(self) -> Tuple[int, int]:
        """!
        Gets the first and last servo depending on the availability of the assembly boards

        @return: Tuple with first_servo, last_servo
        """

        if self.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P3) is True and self.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P4) is True:
            first_servo = 0
            second_servo = 31
        elif self.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P3) is True and self.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P4) is False:
            first_servo = 0
            second_servo = 15
        elif self.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P3) is False and self.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P4) is True:
            first_servo = 16
            second_servo = 31
        else:
            first_servo = -1
            second_servo = -1

        return first_servo, second_servo

    # ------------------------------------------------------------------------------------

    #todo, should be tested first
    def __topboard_io_expander_int_callback(self, _gpio: int) -> None:
        """!
        Callback of interrupt service routine. This routine will be called when the IO expander interrupt fires
        @param _gpio: The GPIO nr which caused the interrupt. (Just for information purpose)
        @return: None

        Should call shutdown_pin_triggered, when 1 sec after triggering still is high, and  2 sec after trigger is low
        """

        # if _gpio is POWER_SHUTDOWN_PIN_IO_TOPBOARD:      # first pin
        #     if self.__topboard_io_expander.get_io_expander_input(POWER_SHUTDOWN_PIN_IO_TOPBOARD) is True:
        #         time.sleep(1)
        #         if self.__topboard_io_expander.get_io_expander_input(POWER_SHUTDOWN_PIN_IO_TOPBOARD) is True:
        #             time.sleep(1)
        #             if self.__topboard_io_expander.get_io_expander_input(POWER_SHUTDOWN_PIN_IO_TOPBOARD) is False:
        #                 time.sleep(1)
        #                 if self.__power_management is not None:
        #                     self.__power_management.shutdown_pin_triggered()

    # ------------------------------------------------------------------------------------
