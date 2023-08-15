#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from robohatlib.Robohat import Robohat
    from robohatlib import RobohatConstants
    from robohatlib.PwmPlug import PwmPlug
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib.hal.datastructure.Color import Color
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.datastructs.IOStatus import IOStatus

    from testlib.Walk import Walk

    from testlib import TestConfig
    import sys
    import os
    import time

    import warnings

except ImportError:
    print("Failed to import Robohat, or failed to import all dependencies")
    raise

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

def main():
    """!
    Start of our test program
    """

    example = Example()                     # creates the class Example

    try:
        example.start_example()             # starts the example

    except KeyboardInterrupt:               # catch 'CTR-C to get a graceful exit'
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            example.exit_program()         # graceful exit
    print("Exit")


    # --------------------------------------------------------------------------------------

class Example:
    """!
    Our example class.

    The Robohat class will be created.
    The Robohat class will be initialized

    Interrupt callbacks will be set onto the io expanders
    """

    def __init__(self):
        print("################################################")
        print("Starting robohat test routine")
        self.__running = True

        self.__robohat = Robohat(TestConfig.servoassembly_1_config,
                                 TestConfig.servoassembly_2_config,
                                 TestConfig.TOPBOARD_IO_EXPANDER_SW)

        # self.robohat.set_system_alarm_permitted(False)

        self.__robohat.init(TestConfig.SERVOBOARD_1_DATAS_ARRAY,
                            TestConfig.SERVOBOARD_2_DATAS_ARRAY)

        self.__robohat.set_topboard_io_expander_int_callback(self.__test_hat_io_expander_int_callback)
        self.__robohat.set_assemblyboard_1_io_expander_int_callback(self.__test_assemblyboard_1_io_expander_int_callback)
        self.__robohat.set_assemblyboard_2_io_expander_int_callback(self.__test_assemblyboard_2_io_expander_int_callback)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """!
        Should exit this program
        @return: None
        """
        print("Exiting this program")
        self.__robohat.exit_program()
        self.__running = False
        sys.exit(0)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_walk(self) -> None:
        """!
        Single test routine to start walking
        @return: None
        """

        print("Test started")
        self.__robohat.set_led_color(Color.GREEN)

        walk_routine = Walk(self.__robohat)
        walk_routine.start_walking()

        self.__robohat.set_led_color(Color.RED)
        print("Test stopped")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_scan_servos(self) -> None:
        """!
        Displays connected servos.
        Does his by sensing the angle values. It can't find the servo, when the angle sense wire is not connected
        @return None
        """

        if self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P3) == False and self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P4) == False:
            print("No servos available, no assembly board is connected")
        else:
            servo_angles = self.__robohat.get_servo_multiple_angles()

            servo_counter = 0

            for i in range(0, len(servo_angles) ):
                if servo_angles[i] > -1:
                    print("Found connected servo: " + str(i) )
                    servo_counter = servo_counter + 1

            if servo_counter == 0:
                print("Did not found any servos")
            else:
                print("Did found: " + str(servo_counter) + " servos")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def servo_fit(self, _servo_nr: int) -> None:
        self.__robohat.do_servo_fit_formula_readout_vs_angle_single_servo(_servo_nr)


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_test(self) -> None:
        """!
        Single test routine which will drive all the servos, will make a beep sound and changes the color of the Multi-LED
        @return: None
        """

        print("Test started")

        running = True
        counter = 0

        while running:
            self.__robohat.set_led_color(Color.GREEN)
            for i in range(100,1700, 10):
                angle:float = i / 10.0
                self.__robohat.set_servo_multiple_angles([angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle])
            print(self.__robohat.get_servo_multiple_angles())

            time.sleep(5)
            self.__robohat.do_buzzer_beep()

            self.__robohat.set_led_color(Color.RED)
            for i in range(1700,100, -10):
                angle:float = i / 10.0
                self.__robohat.set_servo_multiple_angles([angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle])
            print(self.__robohat.get_servo_multiple_angles())

            time.sleep(5)
            self.__robohat.do_buzzer_beep()
            self.__robohat.do_imu_test()

            counter = counter + 1
            if counter > 10:
                running = False

        print("Test stopped")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def shutdown_power(self) -> None:
        """!
        Function which will shut down the RPi and power down the power supply
        :return:
        """
        self.__robohat.do_system_shutdown()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # noinspection PyMethodMayBeStatic
    def print_help(self) -> None:
        """!
        Print a help page will all known command in this test routine
        @return: None
        """

        print("Available commands are:\n")
        print("shutdown                                            powers the system down")
        print("exit                                                exit the program")
        print("help                                                prints this text")
        print("set servo angle [servo nr] [angle]                  moves servo to the desired angle")
        print("get servo angle [servo nr]                          get servo angle of the desired angle")
        print("get servo angle all                                 get all the servo angels")
        print("get servo adc [servo nr]                            get servo position adc value")
        print("get servo adc all                                   get all the servo position adc values")
        print("get servo connected [servo nr]                      shows if servo is connected")
        print("put servos to sleep                                 puts all servos asleep")
        print("set servo io dir [board nr] [pin nr] [in|out]       set the direction of an io pin of a servo board [0|1]")
        print("get servo io dir [board nr] [pin nr]                get the direction of an io pin of a servo board [0|1]")
        print("set servo io output [board nr] [pin nr] [low|high]  set the pin value of an io pin of a servo board [0|1]")
        print("get servo io input [board nr] [pin nr]              get the pin value of an io pin of a servo board [0|1]")
        print("do servo scan                                       displays all servos connected")
        print("do servo fit [servo nr]                             fits angle with voltage readout servo")
        print("wake up servos                                      wakes all servo up")
        print("are servos sleeping                                 shows information if servos are sleeping")
        print("set led [color]                                     turn on led with its color [WHITE|RED|GREEN|BLUE|YELLOW|PURPLE|ON|OFF")
        print("get led                                             displays the color of the led, or status ON | OFF")
        print("get lib builddate                                   displays date when library was build")
        print("get lib version                                     displays version of the library")
        print("get topboard adc [channel]                          get topboard adc value (channel 3 is divided accu voltage")
        print("get topboard adc all                                get all the topboard adc values")
        print("set topboard io dir [pin nr] [in|out]               set the direction of an io pin on the topboard")
        print("get topboard io dir [pin nr]                        get the direction of an io pin on the topboard")
        print("set topboard io output [pin nr] [low|high]          set the pin value of an io pin on the topboard")
        print("get topboard io input [pin nr]                      get the pin value of an io pin on the topboard")
        print("get accu voltage                                    get voltage of accu")
        print("get accu capacity                                   get capacity of accu")
        print("get accu status                                     get status of accu")
        print("get imu magnetic                                    get magnetic values")
        print("get imu acceleration                                get acceleration values")
        print("get imu gyro                                        get gyro values")
        print("do i2c scan                                         scans the i2c bus")
        print("do buzzer random                                    generate a random sound")
        print("do buzzer slowwoop                                  generate a slowwoop sound")
        print("do buzzer beep                                      generate a beep")
        print("do buzzer freq [frequency]                          generates a sound with requested frequency")
        print("do buzzer stop                                      stop the generation of sound")
        print("do test                                             will start a test")
        print("do walk                                             the robot start to walk")


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def process_set(self, _data_in:str) -> None:
        """!
        Will handle console request with commando 'set'
        @return: None
        """

        data_in_array = _data_in.split(" ")
        command = data_in_array[1]

        if command == "servo" and len(data_in_array) >= 3:
            sub_command = data_in_array[2]
            if sub_command == "angle" and len(data_in_array) == 5:
                servo_nr = int(data_in_array[3])
                angle = float(data_in_array[4])
                self.__robohat.set_servo_single_angle(servo_nr, angle)
                print("set servo angle " + str(servo_nr) + " " + str(angle) )
            elif sub_command == "io":
                io_command = data_in_array[3]
                if io_command == "dir":
                    board_nr = int(data_in_array[4])
                    pin_nr = int(data_in_array[5])
                    value = data_in_array[6]
                    if value == "OUT" or value == "out":
                        stat = self.__robohat.set_servo_io_expander_direction(board_nr, pin_nr, ExpanderDir.OUTPUT)
                        if stat == IOStatus.IO_OK:
                            print("Direction set to output")
                    elif value == "IN" or value == "in":
                        stat = self.__robohat.set_servo_io_expander_direction(board_nr, pin_nr, ExpanderDir.INPUT)
                        if stat == IOStatus.IO_OK:
                            print("Direction set to input")
                    else:
                        print("Syntax error setting direction")
                elif io_command == "output":
                    board_nr = int(data_in_array[4])
                    pin_nr = int(data_in_array[5])
                    value = data_in_array[6]
                    if value == "HIGH" or value == "high":
                        stat = self.__robohat.set_servo_io_expander_output(board_nr, pin_nr, ExpanderStatus.HIGH)
                        if stat == IOStatus.IO_OK:
                            print("Pin set to HIGH")
                    elif value == "LOW" or value == "low":
                        stat = self.__robohat.set_servo_io_expander_output(board_nr, pin_nr, ExpanderStatus.LOW)
                        if stat == IOStatus.IO_OK:
                            print("Pin set to LOW")
                    else:
                        print("Syntax error setting output")
                else:
                    print("syntax error, set servo io command not found")
            else:
                print("syntax error, set servo command not found")
# ------------------------------------------------------------------------------
        elif command == "topboard":
            sub_command = data_in_array[2]
            if sub_command == "io":
               io_command = data_in_array[3]
               if io_command == "dir":
                    pin_nr = int(data_in_array[4])
                    value = data_in_array[5]
                    if value == "OUT" or value == "out":
                        stat = self.__robohat.set_topboard_io_expander_direction(pin_nr, ExpanderDir.OUTPUT)
                        if stat == IOStatus.IO_OK:
                            print("Direction set to output")
                    elif value == "IN" or value == "in":
                        stat = self.__robohat.set_topboard_io_expander_direction(pin_nr, ExpanderDir.INPUT)
                        if stat == IOStatus.IO_OK:
                            print("Direction set to input")
                    else:
                        print("Syntax error setting direction pin")

               elif io_command == "output":
                   pin_nr = int(data_in_array[4])
                   value = data_in_array[5]
                   if value == "HIGH" or value == "high":
                       stat = self.__robohat.set_topboard_io_expander_output(pin_nr, ExpanderStatus.HIGH)
                       if stat == IOStatus.IO_OK:
                            print("Pin set to HIGH")
                   elif value == "LOW" or value == "low":
                       stat = self.__robohat.set_topboard_io_expander_output(pin_nr, ExpanderStatus.LOW)
                       if stat == IOStatus.IO_OK:
                            print("Pin set to LOW")
                   else:
                        print("Syntax error setting pin")
               else:
                   print("syntax error, set topboard io command not found")
            else:
               print("syntax error, set topboard command not found")
# ------------------------------------------------------------------------------
        elif command == "led":
            sub_command = data_in_array[2].upper()
            if sub_command == "OFF":
                self.__robohat.turn_led_off()
            elif sub_command == "ON":
                self.__robohat.turn_led_on()
            elif sub_command == "WHITE":
                self.__robohat.set_led_color(Color.WHITE)
            elif sub_command == "RED":
                self.__robohat.set_led_color(Color.RED)
            elif sub_command == "GREEN":
                self.__robohat.set_led_color(Color.GREEN)
            elif sub_command == "BLUE":
                self.__robohat.set_led_color(Color.BLUE)
            elif sub_command == "YELLOW":
                self.__robohat.set_led_color(Color.YELLOW)
            elif sub_command == "PURPLE":
                self.__robohat.set_led_color(Color.PURPLE)
            else:
                print("syntax error, set color unknown")
# ------------------------------------------------------------------------------
        else:
            print("syntax error, unknown set command")

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

    def process_get(self, _data_in:str) -> None:
        """!
        Will handle console request with commando 'get'
        @return: None
        """
        data_in_array = _data_in.split(" ")
        command = data_in_array[1]
# -------------------------------------------------------------------------------
        if command == "servo" and len(data_in_array) >= 3:
            sub_command = data_in_array[2]
            if sub_command == "angle" and len(data_in_array) == 4:
                parameter_str:str = data_in_array[3]
                if parameter_str.isnumeric():
                    servo_nr = int(parameter_str)
                    value = self.__robohat.get_servo_single_angle(servo_nr)
                    if value != -1:
                        print("angle of servo " + str(servo_nr) + " is: " + str(value) + "°" )
                elif parameter_str == "all":
                    value = self.__robohat.get_servo_multiple_angles()
                    if not value:
                        print("There a no servos attached")
                    else:
                        print("angles of servos: " + str(value))
                else:
                    print("syntax error")
            elif sub_command == "adc":
                parameter_str: str = data_in_array[3]
                if parameter_str.isnumeric():
                    servo_nr = int(data_in_array[3])
                    value = self.__robohat.get_servo_adc_single_channel(servo_nr)
                    if value != -1:
                        print("adc of servo " + str(servo_nr) + " is: " + str(value) + "V" )
                elif parameter_str == "all":
                    value = self.__robohat.get_servo_adc_multiple_channels()
                    if not value:
                        print("There a no servos attached")
                    else:
                        print("adc volts of servos: " + str(value))
                else:
                    print("syntax error")
            elif sub_command == "connected":
                servo_nr = int(data_in_array[3])
                value = self.__robohat.get_servo_is_connected(servo_nr)
                if value is True:
                    print("Servo " + str(servo_nr) + " is connected")
                else:
                    print("Servo " + str(servo_nr) + " NOT is connected")
            elif sub_command == "io":
                io_command = data_in_array[3]
                if io_command == "dir":
                    board_nr = int(data_in_array[4])
                    pin_nr = int(data_in_array[5])
                    value = self.__robohat.get_servo_io_expander_direction(board_nr, pin_nr)
                    print(value)
                elif io_command == "input":
                    board_nr = int(data_in_array[4])
                    pin_nr = int(data_in_array[5])
                    value = self.__robohat.get_servo_io_expander_input(board_nr, pin_nr)
                    print(value)
                else:
                    print("syntax error, get servo io ")
            else:
                print("syntax error, get servo")
# -------------------------------------------------------------------------------
        elif command == "topboard" and len(data_in_array) >= 3:
            sub_command = data_in_array[2]
            if sub_command == "adc":
                parameter_str: str = data_in_array[3]
                if parameter_str.isnumeric():
                    channel_nr = int(parameter_str)
                    value = self.__robohat.get_topboard_adc_single_channel(channel_nr)
                    if value != -1:
                        print("adc hat channel " + str(channel_nr) + " is: " + str(value) + "V" )
                elif parameter_str == "all":
                    value = self.__robohat.get_topboard_adc_multiple_channels()
                    print("adc hat volts of channels: " + str(value))
                else:
                    print("syntax error at hat: " + parameter_str )
            elif sub_command == "io":
                io_command = data_in_array[3]
                if io_command == "dir":
                    pin_nr = int(data_in_array[4])
                    value = self.__robohat.get_topboard_io_expander_direction(pin_nr)
                    print(value)
                elif io_command == "input":
                    pin_nr = int(data_in_array[4])
                    value = self.__robohat.get_topboard_io_expander_input(pin_nr)
                    print(value)
                else:
                    print("syntax error, unknown hat io command")
            else:
                print("syntax error, unknown hat command")
# -------------------------------------------------------------------------------
        elif command == "led":
            value = self.__robohat.get_led_color()
            if value is Color.OFF:
                print("Led is OFF")
            else:
                print(value)
# -------------------------------------------------------------------------------
        elif command == "lib" and len(data_in_array) >= 3:
            sub_command = data_in_array[2]
            if sub_command == "builddate":
                print("build date of Robohat lib is: " + self.__robohat.get_lib_build_date())
            elif sub_command == "version":
                print("version of Robohat lib is: " + self.__robohat.get_lib_version())
            else:
                print("syntax error")
# -------------------------------------------------------------------------------
        elif command == "accu" and len(data_in_array) >= 3:
            sub_command = data_in_array[2]
            if sub_command == "voltage":
                value = self.__robohat.get_accu_voltage()
                print("accu voltage is: " + str(value) + " V")
            elif sub_command == "capacity":
                value = self.__robohat.get_accu_percentage_capacity()
                print("accu capacity is: " + str(value) + " %")
            elif sub_command == "status":
                value = self.__robohat.get_accu_status()
                print(value)
            else:
                print("syntax error")
# -------------------------------------------------------------------------------
        elif command == "imu" and len(data_in_array) >= 3:
            sub_command = data_in_array[2]
            if sub_command == "magnetic":
                value = self.__robohat.get_imu_magnetic_fields()
                if value is not None:
                    print("IMU magnetic: " + str(value) )
                else:
                    print("IMU not present")
            elif sub_command == "acceleration":
                value = self.__robohat.get_imu_acceleration()
                if value is not None:
                    print("IMU acceleration: " + str(value) )
                else:
                    print("IMU not present")
            elif sub_command == "gyro":
                value = self.__robohat.get_imu_gyro()
                if value is not None:
                    print("IMU gyro: " + str(value) )
                else:
                    print("IMU not present")
            else:
                print("syntax error")
        else:
            print("syntax error")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def process_do(self, _data_in:str) -> None:
        """!
        Will handle console request with commando 'do'
        @return: None
        """
        data_in_array = _data_in.split(" ")

        command = data_in_array[1]
        if command == "i2c":
            sub_command = data_in_array[2]
            if sub_command == "scan":
                self.__robohat.do_i2c_scan()
            else:
                print("syntax error do i2c")
# -------------------------------------------------------
        elif command == "buzzer":
            sub_command = data_in_array[2]
            if sub_command == "random":
                self.__robohat.do_buzzer_random()
            elif sub_command == "slowwoop":
                self.__robohat.do_buzzer_slowwoop()
            elif sub_command == "beep":
                self.__robohat.do_buzzer_beep()
            elif sub_command == "freq":
                freq_str = data_in_array[3]
                if freq_str.isnumeric():
                    freq = int(freq_str)
                    self.__robohat.do_buzzer_freq(freq)
            elif sub_command == "stop":
                self.__robohat.do_buzzer_release()
            else:
                print("syntax error do buzzer")
# -------------------------------------------------------
        elif command == "servo":
            sub_command = data_in_array[2]
            if sub_command == "scan":
                self.do_scan_servos()
            elif sub_command == "fit" and len(data_in_array) >= 4:
                servo_nr = int(data_in_array[3])
                self.servo_fit(servo_nr)


# -------------------------------------------------------

        elif command == "test":
            self.do_test()
        elif command == "walk":
            self.do_walk()

        else:
            print("syntax error")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def process_commands(self, _command:str) -> None:
        """!
        Will handle console request
        @param _command: console input
        @return: None
        """
        if _command == "exit":
            self.exit_program()

        elif _command == "help":
            self.print_help()

        elif _command == "shutdown":
            self.shutdown_power()

        elif _command.startswith("set"):
            self.process_set(_command)

        elif _command.startswith("get"):
            self.process_get(_command)

        elif _command.startswith("do"):
            self.process_do(_command)

        elif _command == "are servos sleeping":
            value = self.__robohat.are_servos_sleeping()
            if value is True:
                print("Servos are sleeping")
            else:
                print("Servos are a wake")
        elif _command == "put servos to sleep":
            self.__robohat.put_servo_to_sleep()
            print("servos went to sleep")
        elif _command == "wake up servos":
            self.__robohat.wakeup_servo()
            print("servos are a wake")


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_example(self) -> None:
        """!
        Start this example
        @return: None
        """
        print("\n\nWaiting for your input (type help + [RETURN] for more the command list\n\n")

        while self.__running is True:
            inp = input()
            self.process_commands(inp)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    # some test routines
    def __test_hat_io_expander_int_callback(self, _gpi_nr: int) -> None:
        """!
        Just a test callback, for the hat_io_expander
        due to 'self.robohat.set_hat_io_expander_int_callback(self.__test_hat_io_expander_int_callback)' this function is
        added to the interrupt handler and wil be executed when the interrupt is triggered

        @param _gpi_nr (int) mr of the callback gpio pin
        @return None
        """
        print("__test_hat_io_expander_int_callback by: " + str(_gpi_nr))
        self.__robohat.do_buzzer_beep()

    # some test routines
    def __test_assemblyboard_1_io_expander_int_callback(self, _gpi_nr: int) -> None:
        """!
        Just a test callback, for the hat_io_expander
        self.robohat.set_assemblyboard_1_io_expander_int_callback(self.__test_assemblyboard_1_io_expander_int_callback)
        added to the interrupt handler and wil be executed when the interrupt is triggered

        @param _gpi_nr (int) nr of the callback gpio pin
        @return None
        """
        print("__test_assemblyboard1_io_expander_int_callback by: " + str(_gpi_nr))
        self.__robohat.do_buzzer_beep()

    def __test_assemblyboard_2_io_expander_int_callback(self, _gpi_nr: int) -> None:
        """!
        Just a test callback, for the hat_io_expander
        self.robohat.set_assemblyboard_2_io_expander_int_callback(self.__test_assemblyboard_1_io_expander_int_callback)
        added to the interrupt handler and wil be executed when the interrupt is triggered

        @param _gpi_nr (int) nr of the callback gpio pin
        @return None
        """
        print("__test_assemblyboard2_io_expander_int_callback by: " + str(_gpi_nr))
        self.__robohat.do_buzzer_beep()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------