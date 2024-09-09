"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

"""

from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from robohatlib.Robohat import Robohat
    from robohatlib import RobohatConstants
    from robohatlib.hal.assemblyboard.PwmPlug import PwmPlug
    from robohatlib import RobohatConfig
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib.hal.datastructure.Color import Color
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.datastructs.IOStatus import IOStatus

    from testlib import TestConfig

    import sys
    import os
    import time

except ImportError:
    print("Failed to import all dependencies for SerTestClass")
    raise

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

SUPER_USER_MAX_MOVE = 170
SUPER_USER_MIN_MOVE = 10

NORMAL_USER_MAX_MOVE = 160
NORMAL_USER_MIN_MOVE = 20

# --------------------------------------------------------------------------------------


class SerTestClass:
    """!
    Our example class.

    The Robohat class will be created.
    The Robohat class will be initialized
    """

    def __init__(self):
        """!
        Constructor of this test class
        """
        print("################################################")
        print("Starting robohat servo test routine")
        self.__running = True

        self.__robohat = Robohat(TestConfig.SERVOASSEMBLY_1_CONFIG, TestConfig.SERVOASSEMBLY_2_CONFIG, TestConfig.TOPBOARD_ID_SWITCH)
        self.__robohat.init(TestConfig.SERVOBOARD_1_DATAS_LIST, TestConfig.SERVOBOARD_2_DATAS_LIST)
        self.__robohat.do_buzzer_beep()
        self.__i_am_super_user = False

        self.__robohat.start_servo_drivers()

        print("\n")

        if len(sys.argv) > 1:
            self.__i_am_super_user = True
            print("You are a superuser, warning")
            self.__limit_min = SUPER_USER_MIN_MOVE
            self.__limit_max = SUPER_USER_MAX_MOVE
        else:
            self.__limit_min = NORMAL_USER_MIN_MOVE
            self.__limit_max = NORMAL_USER_MAX_MOVE

        print("limits are from " + str(self.__limit_min) + " till " + str(self.__limit_max) )

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start(self) -> None:
        """!
        Starts the infinite loop which scans the keyboard
        @return: None
        """
        self.__ser_test_help()

        while self.__running is True:
            inp = input()
            self.__process_commands(inp)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic
    def __ser_test_help(self) -> None:
        """!
        Will print available commands
        @return: None
        """

        print("\n")
        print("1 show all connected servos")
        print("2 calibrate servos")
        print("3 read out the angles of the servos")
        print("4 move servos to " + str(self.__limit_min) + " °")
        print("5 move servos to 90 °")
        print("6 move servos to " + str(self.__limit_max) + " °")
        print("7 topboard OUTPUT test ")
        print("8 assembly boards OUTPUT test ")
        print("l for led test ")
        print("v show voltages of all servo adcs")
        print("t toggle SERVO update mode between DIRECT or PERIODICALLY")
        print("b sounds the buzzer")
        print("c test camera")

        print("\n")
        print("x for exit")
        print("\n")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __process_commands(self, _command: str) -> None:
        """!
        Will handle console request
        @param _command: console input
        @return: None
        """
        if _command == "1":
            self.__servo_show_connected()
        elif _command == "v":
            self.__servo_show_adc_voltages()
        elif _command == "2":
            self.__servo_calibrate()
        elif _command == "3":
            self.__servo_read_angle()
        elif _command == "4":
            self.__servo_move(self.__limit_min)
        elif _command == "5":
            self.__servo_move(90.0)
        elif _command == "6":
            self.__servo_move(self.__limit_max)
        elif _command == "7":
            self.__topboard_running_light()
        elif _command == "8":
            self.__assembly_boards_running_light()

        elif _command == "l":
            self.__led_test()
        elif _command == "t":
            self.__toggle_direct_update_mode()
        elif _command == "b":
            self.__sound_the_buzzer()
        elif _command == "c":
            self.__test_the_camera()

        # --------------------------------------------------------------------------------------
        elif _command == "x":
            self.exit_program()
        else:
            self.__ser_test_help()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __servo_show_connected(self) -> None:
        angles = self.__robohat.get_servo_multiple_angles()

        servo_counter = 0
        for servo_nr in range(0, len(angles)):
            pos = angles[servo_nr]
            if pos != -1:
                print("Servo " + str(servo_nr) + " is connected")
                servo_counter = servo_counter + 1

        if servo_counter == 0:
            print("No servos are found")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __servo_show_adc_voltages(self) -> None:
        """!
        Shows the servo adc voltages
        @return: None
        """
        voltages = self.__robohat.get_servo_adc_multiple_channels()
        for servo_nr in range(0, len(voltages)):
            voltage = voltages[servo_nr]
            print("Servo " + str(servo_nr) + ": " + str(voltage) + " V")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __servo_calibrate(self) -> None:
        """!
        Will calibrate the adc of servo 0
        @return: None
        """
        print("Going to calibrate the servos. Please be patient...")
        self.__robohat.do_servo_fit_formula_readout_vs_angle_multiple_servos(self.__limit_min, self.__limit_max)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __servo_read_angle(self) -> None:
        """!
        Will read the angle of servo 0
        @return: None
        """

        angles = self.__robohat.get_servo_multiple_angles()
        for i in range(0, len(angles)):
            pos = angles[i]
            if pos == -1:
                print("Servo " + str(i) + " is not connected")
            else:
                print("Servo " + str(i) + " position is " + str(pos) + " °")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __servo_move(self, _degree: float) -> None:
        """!
        Will read the angle of servo 0
        @paramL _degree wanted degree of servo
        @return: None
        """

        time_to_servo = self.__robohat.get_servo_us_time(_degree)

        self.__robohat.set_servo_multiple_angles(
            [
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
                _degree,
            ]
        )

        print(
            "Angles of the servos should be: "
            + str(_degree)
            + "°"
            + " time: "
            + str(int(time_to_servo))
            + " uS"
        )

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __toggle_direct_update_mode(self) -> None:
        """!
        Toggles the servo update mode
        @return: None
        """
        mode = self.__robohat.get_servo_is_direct_mode()
        if mode is False:
            print("setting SERVO update mode to DIRECT")
            self.__robohat.set_servo_direct_mode(True)
        else:
            print("setting SERVO update mode to PERIODICALLY")
            self.__robohat.set_servo_direct_mode(False)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __topboard_running_light(self) -> None:
        """!
        Sets the IO of the topboard, in sequence. When leds are attached you will get a running light
        @return: None
        """
        print("Starting topboard OUTPUT test")

        for pin_nr_dir in range(8):
            self.__robohat.set_topboard_io_expander_direction(
                pin_nr_dir, ExpanderDir.OUTPUT
            )

        pin_high_nr = 0
        for loop_counter in range(3):
            for led_counter in range(8):
                for pin_nr in range(8):
                    self.__robohat.set_topboard_io_expander_output(
                        pin_nr, ExpanderStatus.LOW
                    )

                self.__robohat.set_topboard_io_expander_output(
                    pin_high_nr, ExpanderStatus.HIGH
                )
                pin_high_nr = pin_high_nr + 1
                if pin_high_nr >= 8:
                    pin_high_nr = 0

                print("--> " + str(loop_counter) + " LED GP:" + str(led_counter))
                time.sleep(1)

        for pin_nr in range(8):
            self.__robohat.set_topboard_io_expander_output(pin_nr, ExpanderStatus.LOW)

        print("Ready topboard OUTPUT test")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __assembly_boards_running_light(self) -> None:
        """
        Sets the IO of the attached assembly boards, in sequence. When leds are attached you will get a running light
        @return: None
        """

        print("Starting assembly boards OUTPUT test")

        for pin_nr_dir in range(4, 7):
            if (
                self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P3)
                is True
            ):
                self.__robohat.set_servo_io_expander_direction(
                    PwmPlug.PWMPLUG_P3, pin_nr_dir, ExpanderDir.OUTPUT
                )
            if (
                self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P4)
                is True
            ):
                self.__robohat.set_servo_io_expander_direction(
                    PwmPlug.PWMPLUG_P4, pin_nr_dir, ExpanderDir.OUTPUT
                )

        pin_high_nr = 4
        for loop_counter in range(3):
            for led_counter in range(4, 7):
                for pin_nr in range(4, 7):
                    if (
                        self.__robohat.get_assemblyboard_is_connected(
                            PwmPlug.PWMPLUG_P3
                        )
                        is True
                    ):
                        self.__robohat.set_servo_io_expander_output(
                            PwmPlug.PWMPLUG_P3, pin_nr, ExpanderStatus.LOW
                        )
                    if (
                        self.__robohat.get_assemblyboard_is_connected(
                            PwmPlug.PWMPLUG_P4
                        )
                        is True
                    ):
                        self.__robohat.set_servo_io_expander_output(
                            PwmPlug.PWMPLUG_P4, pin_nr, ExpanderStatus.LOW
                        )

                if (
                    self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P3)
                    is True
                ):
                    self.__robohat.set_servo_io_expander_output(
                        PwmPlug.PWMPLUG_P3, pin_high_nr, ExpanderStatus.HIGH
                    )
                if (
                    self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P4)
                    is True
                ):
                    self.__robohat.set_servo_io_expander_output(
                        PwmPlug.PWMPLUG_P4, pin_high_nr, ExpanderStatus.HIGH
                    )

                pin_high_nr = pin_high_nr + 1
                if pin_high_nr >= 7:
                    pin_high_nr = 4

                if (
                    self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P3)
                    is True
                ):
                    print(
                        "Plug P3: --> "
                        + str(loop_counter)
                        + " LED GP:"
                        + str(led_counter)
                    )
                if (
                    self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P4)
                    is True
                ):
                    print(
                        "Plug P4: --> "
                        + str(loop_counter)
                        + " LED GP:"
                        + str(led_counter)
                    )
                time.sleep(1)

        for pin_nr in range(4, 7):
            if (
                self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P3)
                is True
            ):
                self.__robohat.set_servo_io_expander_output(
                    PwmPlug.PWMPLUG_P3, pin_nr, ExpanderStatus.LOW
                )
            if (
                self.__robohat.get_assemblyboard_is_connected(PwmPlug.PWMPLUG_P4)
                is True
            ):
                self.__robohat.set_servo_io_expander_output(
                    PwmPlug.PWMPLUG_P4, pin_nr, ExpanderStatus.LOW
                )

        print("Ready assembly boards OUTPUT test")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __led_test(self) -> None:
        """!
        Do a LED test
        @return: None
        """

        print("Starting LED test")
        self.__robohat.set_led_color(Color.RED)
        print("LED: RED")
        time.sleep(1)
        self.__robohat.set_led_color(Color.GREEN)
        print("LED: GREEN")
        time.sleep(1)
        self.__robohat.set_led_color(Color.YELLOW)
        print("LED: YELLOW")
        time.sleep(1)
        self.__robohat.set_led_color(Color.BLUE)
        print("LED: BLUE")
        time.sleep(1)
        self.__robohat.set_led_color(Color.WHITE)
        print("Ready LED test")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __sound_the_buzzer(self) -> None:
        """!
        Make some sound with the buzzer
        @return: None
        """
        self.__robohat.do_buzzer_random()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __test_the_camera(self) -> None:
        """!
        Test the camera
        @return: None
        """
        self.__robohat.test_camera()

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

def main():
    """!
    Start of our servo test program
    """

    ser_test = SerTestClass()  # creates the class Example

    try:
        ser_test.start()  # starts the example

    except KeyboardInterrupt:  # catch 'CTR-C to get a graceful exit'
        print("Interrupted")
        try:
            sys.exit(130)
        except SystemExit:
            ser_test.exit_program()  # graceful exit
    print("Exit")

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
