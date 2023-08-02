#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from robohatlib.Robohat import Robohat
    from robohatlib import RobohatConstants
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib.hal.datastructure.Color import Color
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    from robohatlib.driver_ll.datastructs.IOStatus import IOStatus

    from testlib.Walk import Walk

    import TestConfig
    import sys
    import os
    import time

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

    ser_test = SerTest()                     # creates the class Example

    try:
        ser_test.start()             # starts the example

    except KeyboardInterrupt:               # catch 'CTR-C to get a graceful exit'
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            ser_test.exit_program()         # graceful exit
    print("Exit")


    # --------------------------------------------------------------------------------------

class SerTest:
    """!
    Our example class.

    The Robohat class will be created.
    The Robohat class will be initialized
    """

    def __init__(self):
        print("################################################")
        print("Starting robohat servo test routine")
        self.__running = True

        self.__robohat = Robohat(TestConfig.servoassembly_1_config,
                                 TestConfig.servoassembly_2_config,
                                 TestConfig.TOPBOARD_IO_EXPANDER_SW)

        self.__robohat.init(TestConfig.SERVOBOARD_1_DATAS_ARRAY,
                            TestConfig.SERVOBOARD_2_DATAS_ARRAY)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start(self) -> None:
        help()

        while self.__running is True:

            inp = input()
            self.process_commands(inp)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def help(self) -> None:
        """!
        Will print available commands
        @return: None
        """
        print("\n")

        print("1 for servo 0, calibrate")
        print("2 for servo 0, move to 20 degree")
        print("3 for servo 0, move to 90 degree")
        print("4 for servo 0, move to 160 degree")
        print("5 for exit")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def process_commands(self, _command:str) -> None:
        """!
        Will handle console request
        @param _command: console input
        @return: None
        """

        if _command == "1":
            self.servo_calibrate()
        elif _command == "2":
            self.servo_read_angle()
        elif _command == "3":
            self.servo_move(20.0)
        elif _command == "4":
            self.servo_move(90.0)
        elif _command == "5":
            self.servo_move(160.0)
        elif _command == "6":
            self.exit_program()
        else:
            self.help()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def servo_calibrate(self) -> None:
        """!
        Will calibrate the adc of servo 0
        @return: None
        """
        self.__robohat.do_servo_fit_formula_readout_vs_angle(0)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def servo_read_angle(self) -> None:
        """!
        Will read the angle of servo 0
        @return: None
        """

        value = self.__robohat.get_servo_single_angle(0)
        if value != -1:
            print("angle of servo " + str(0) + " is: " + str(value) + "°")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def servo_move(self, _degree: float) -> None:
        """!
        Will read the angle of servo 0
        @paramL _degree wanted degree of servo
        @return: None
        """
        self.__robohat.set_servo_single_angle(0, _degree)

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

