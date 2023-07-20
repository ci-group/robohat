from __future__ import absolute_import, division, print_function, unicode_literals



try:
    from robohatlib.Robohat import Robohat
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib.hal.datastructure.Color import Color
    from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir
    from robohatlib.hal.datastructure.ExpanderStatus import ExpanderStatus
    import main_config
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
    example = Example()

    try:
        example.start_example()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            example.exit_program()



    print("Exit")


    # --------------------------------------------------------------------------------------
class Example:
    def __init__(self):
        print("################################################")
        print("Starting robohat test routine")
        self.running = True

        self.robohat = Robohat(main_config.servoassembly_1_config,
                               main_config.servoassembly_2_config,
                               main_config.TOPBOARD_IO_EXPANDER_SW)

        # self.robohat.set_system_alarm_permitted(False)

        self.robohat.init(main_config.SERVOBOARD_1_DATAS_ARRAY,
                          main_config.SERVOBOARD_2_DATAS_ARRAY)


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def exit_program(self) -> None:
        """!
        Should stop this program
        @return: None
        """
        print("Exiting this program")
        self.robohat.exit_program()
        self.running = False
        sys.exit(0)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_test(self):
        print("Test started")

        running = True
        counter = 0

        while running:
            self.robohat.set_led_color(Color.GREEN)
            for i in range(100,1700, 10):
                angle:float = i / 10.0
                self.robohat.set_servo_multiple_angles([angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle])
            print(self.robohat.get_servo_multiple_angles())

            time.sleep(5)
            self.robohat.do_buzzer_beep()

            self.robohat.set_led_color(Color.RED)
            for i in range(1700,100, -10):
                angle:float = i / 10.0
                self.robohat.set_servo_multiple_angles([angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle])
            print(self.robohat.get_servo_multiple_angles())

            time.sleep(5)
            self.robohat.do_buzzer_beep()
            self.robohat.do_imu_test()

            counter = counter + 1
            if counter > 10:
                running = False

        print("Test stopped")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def shutdown_power(self) -> None:
        self.robohat.do_system_shutdown()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def print_help(self) -> None:
        """!
        Print a help page
        @return: None
        """
        print("Available commands are:\n")
        print("shutdown                                       powers the system down")
        print("exit                                           exit the program")
        print("help                                           prints this text")
        print("set servo angle [servo nr] [angle]             moves servo to the desired angle")
        print("get servo angle [servo nr]                     get servo angle of the desired angle")
        print("get servo angle all                            get all the servo angels")
        print("get servo adc [servo nr]                       get servo position adc value")
        print("get servo adc all                              get all the servo position adc values")
        print("get servo connected [servo nr]                 shows if servo is connected")
        print("put servos to sleep                            puts all servos asleep")

        print("set servo io dir [pin nr] [in|out]             set the direction of an io pin of a servo board")
        print("get servo io dir [pin nr]                      get the direction of an io pin of a servo board")
        print("set servo io output [pin nr] [0|1]             set the pin value of an io pin of a servo board")
        print("get servo io input [pin nr]                    get the pin value of an io pin of a servo board")

        print("wake up servos                                 wakes all servo up")
        print("are servos sleeping                            shows information if servos are sleeping")

        print("set led [color]                                turn on led with its color [WHITE|RED|GREEN|BLUE|YELLOW|PURPLE|ON|OFF")
        print("get led                                        displays the color of the led, or status ON | OFF")

        print("get lib builddate                              displays date when library was build")
        print("get lib version                                displays version of the library")

        print("get topboard adc [channel]                     get topboard adc value (channel 3 is divided accu voltage")
        print("get topboard adc all                           get all the topboard adc values")
        print("set topboard io dir [pin nr] [in|out]          set the direction of an io pin on the topboard")
        print("get topboard io dir [pin nr]                   get the direction of an io pin on the topboard")
        print("set topboard io output [pin nr] [0|1]          set the pin value of an io pin on the topboard")
        print("get topboard io input [pin nr]                 get the pin value of an io pin on the topboard")

        print("get accu voltage                               get voltage of accu")
        print("get accu capacity                              get capacity of accu")
        print("get accu status                                get status of accu")

        print("get imu magnetic                               get magnetic values")
        print("get imu acceleration                           get acceleration values")
        print("get imu gyro                                   get gyro values")

        print("do i2c scan                                    scans the i2c bus")

        print("do buzzer random                               generate a random sound")
        print("do buzzer slowwoop                             generate a slowwoop sound")
        print("do buzzer beep                                 generate a beep")
        print("do buzzer freq [frequency]                     generates a sound with requested frequency")
        print("do buzzer stop                                 stop the generation of sound")

        print("do test                                        will start a test")

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

        if command == "servo":
            sub_command = data_in_array[2]
            if sub_command == "angle":
                servo_nr = int(data_in_array[3])
                angle = float(data_in_array[4])
                self.robohat.set_servo_single_angle(servo_nr, angle)
            elif sub_command == "io":
                io_command = data_in_array[3]
                if io_command == "dir":
                    board_nr = int(data_in_array[4])
                    pin_nr = int(data_in_array[5])
                    value = data_in_array[6]
                    if value is "out":
                        self.robohat.set_servo_io_expander_direction(board_nr, pin_nr, ExpanderDir.OUTPUT)
                    else:
                        self.robohat.set_servo_io_expander_direction(board_nr, pin_nr, ExpanderDir.INPUT)
                elif io_command == "output":
                    board_nr = int(data_in_array[4])
                    pin_nr = int(data_in_array[4])
                    value = data_in_array[6]
                    if value is "0":
                        self.robohat.set_servo_io_expander_output(board_nr, pin_nr, ExpanderStatus.LOW)
                    else:
                        self.robohat.set_servo_io_expander_output(board_nr, pin_nr, ExpanderStatus.HIGH)
                else:
                    print("syntax error, set servo io command not found")
            else:
                print("syntax error, set servo command not found")
# ------------------------------------------------------------------------------
        elif command == "topboard":
            sub_command = data_in_array[2]
            if sub_command == "io":
               io_command = int(data_in_array[3])
               if io_command == "dir":
                    pin_nr = int(data_in_array[4])
                    value = data_in_array[5]
                    if value is "out":
                        self.robohat.set_hat_io_expander_direction(pin_nr, ExpanderDir.OUTPUT)
                    else:
                        self.robohat.set_hat_io_expander_direction(pin_nr, ExpanderDir.INPUT)
               elif io_command == "out":
                   pin_nr = int(data_in_array[4])
                   value = data_in_array[5]
                   if value is "0":
                       self.robohat.set_hat_io_expander_output(pin_nr, ExpanderStatus.LOW)
                   else:
                       self.robohat.set_hat_io_expander_output(pin_nr, ExpanderStatus.HIGH)
               else:
                   print("syntax error, set hat io command not found")
            else:
               print("syntax error, set hat command not found")
# ------------------------------------------------------------------------------
        elif command == "led":
            sub_command = data_in_array[2].upper()
            if sub_command == "OFF":
                self.robohat.turn_led_off()
            elif sub_command == "ON":
                self.robohat.turn_led_on()
            elif sub_command == "WHITE":
                self.robohat.set_led_color(Color.WHITE)
            elif sub_command == "RED":
                self.robohat.set_led_color(Color.RED)
            elif sub_command == "GREEN":
                self.robohat.set_led_color(Color.GREEN)
            elif sub_command == "BLUE":
                self.robohat.set_led_color(Color.BLUE)
            elif sub_command == "YELLOW":
                self.robohat.set_led_color(Color.YELLOW)
            elif sub_command == "PURPLE":
                self.robohat.set_led_color(Color.PURPLE)
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
        if command == "servo":
            sub_command = data_in_array[2]
            if sub_command == "angle":
                parameter_str:str = data_in_array[3]
                if parameter_str.isnumeric():
                    servo_nr = int(parameter_str)
                    value = self.robohat.get_servo_single_angle(servo_nr)
                    if value != -1:
                        print("angle of servo " + str(servo_nr) + " is: " + str(value) + "°" )
                elif parameter_str == "all":
                    value = self.robohat.get_servo_multiple_angles()
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
                    value = self.robohat.get_servo_adc_single_channel(servo_nr)
                    if value != -1:
                        print("adc of servo " + str(servo_nr) + " is: " + str(value) + "V" )
                elif parameter_str == "all":
                    value = self.robohat.get_servo_adc_multiple_channels()
                    if not value:
                        print("There a no servos attached")
                    else:
                        print("adc volts of servos: " + str(value))
                else:
                    print("syntax error")
            elif sub_command == "connected":
                servo_nr = int(data_in_array[3])
                value = self.robohat.get_servo_is_connected(servo_nr)
                if value is True:
                    print("Servo " + str(servo_nr) + " is connected")
                else:
                    print("Servo " + str(servo_nr) + " NOT is connected")
            elif sub_command == "io":
                io_command = data_in_array[3]
                if io_command == "dir":
                    board_nr = int(data_in_array[4])
                    pin_nr = int(data_in_array[4])
                    value = self.robohat.get_servo_io_expander_direction(board_nr, pin_nr)
                    print(value)
                elif io_command == "input":
                    board_nr = int(data_in_array[4])
                    pin_nr = int(data_in_array[4])
                    value = self.robohat.get_servo_io_expander_input(board_nr, pin_nr)
                    print(value)
                else:
                    print("syntax error, get servo io ")
            else:
                print("syntax error, get servo")
# -------------------------------------------------------------------------------
        elif command == "topboard":
            sub_command = data_in_array[2]
            if sub_command == "adc":
                parameter_str: str = data_in_array[3]
                if parameter_str.isnumeric():
                    channel_nr = int(parameter_str)
                    value = self.robohat.get_hat_adc_single_channel(channel_nr)
                    if value != -1:
                        print("adc hat channel " + str(channel_nr) + " is: " + str(value) + "V" )
                elif parameter_str == "all":
                    value = self.robohat.get_hat_adc_multiple_channels()
                    print("adc hat volts of channels: " + str(value))
                else:
                    print("syntax error at hat: " + parameter_str )
            elif sub_command == "io":
                io_command = data_in_array[3]
                if io_command == "dir":
                    pin_nr = int(data_in_array[4])
                    value = self.robohat.get_hat_io_expander_direction(pin_nr)
                    print(value)
                elif io_command == "input":
                    pin_nr = int(data_in_array[4])
                    value = self.robohat.get_hat_io_expander_input(pin_nr)
                    print("topboard io: " + str(value) )
                else:
                    print("syntax error, unknown hat io command")
            else:
                print("syntax error, unknown hat command")
# -------------------------------------------------------------------------------
        elif command == "led":
            value = self.robohat.get_led_color()
            if value is Color.OFF:
                print("Led is OFF")
            else:
                print(value)
# -------------------------------------------------------------------------------
        elif command == "lib":
            sub_command = data_in_array[2]
            if sub_command == "builddate":
                print("build date of Robohat lib is: " + self.robohat.get_lib_build_date())
            elif sub_command == "version":
                print("version of Robohat lib is: " + self.robohat.get_lib_version())
            else:
                print("syntax error")
# -------------------------------------------------------------------------------
        elif command == "accu":
            sub_command = data_in_array[2]
            if sub_command == "voltage":
                value = self.robohat.get_accu_voltage()
                print("accu voltage is: " + str(value) + " V")
            elif sub_command == "capacity":
                value = self.robohat.get_accu_percentage_capacity()
                print("accu capacity is: " + str(value) + " %")
            elif sub_command == "status":
                value = self.robohat.get_accu_status()
                print(value)
            else:
                print("syntax error")
# -------------------------------------------------------------------------------
        elif command == "imu":
            sub_command = data_in_array[2]
            if sub_command == "magnetic":
                value = self.robohat.get_imu_magnetic_fields()
                if value is not None:
                    print("IMU magnetic: " + str(value) )
                else:
                    print("IMU not present")
            elif sub_command == "acceleration":
                value = self.robohat.get_imu_acceleration()
                if value is not None:
                    print("IMU acceleration: " + str(value) )
                else:
                    print("IMU not present")
            elif sub_command == "gyro":
                value = self.robohat.get_imu_gyro()
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
                self.robohat.do_i2c_scan()
            else:
                print("syntax error do i2c")

        elif command == "buzzer":
            sub_command = data_in_array[2]
            if sub_command == "random":
                self.robohat.do_buzzer_random()
            elif sub_command == "slowwoop":
                self.robohat.do_buzzer_slowwoop()
            elif sub_command == "beep":
                self.robohat.do_buzzer_beep()
            elif sub_command == "freq":
                freq_str = data_in_array[3]
                if freq_str.isnumeric():
                    freq = int(freq_str)
                    self.robohat.do_buzzer_freq(freq)
            elif sub_command == "stop":
                self.robohat.do_buzzer_release()
            else:
                print("syntax error do buzzer")
        elif command == "test":
            self.do_test()

        else:
            print("syntax error")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_example(self) -> None:
        """!
        Start this example
        @return: None
        """
        print("\n\nWaiting for your input (type help + [RETURN] for more the command list\n\n")

        while self.running is True:
            inp = input()
            self.process_commands(inp)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def process_commands(self, _command:str):
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
            value = self.robohat.are_servos_sleeping()
            if value is True:
                print("Servos are sleeping")
            else:
                print("Servos are a wake")
        elif _command == "put servos to sleep":
            self.robohat.put_servo_to_sleep()
            print("servos went to sleep")
        elif _command == "wake up servos":
            self.robohat.wakeup_servo()
            print("servos are a wake")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------