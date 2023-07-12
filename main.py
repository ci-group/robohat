
from __future__ import absolute_import, division, print_function, unicode_literals

import time


try:
    from robohatlib.Robohat import Robohat
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib.hal.datastructure.Color import Color
    import sys
    import main_config


except ImportError:
    print("Failed to import Robohat, or failed to import all dependencies")
    raise

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

def main():
    example = Example()
    example.start_example()

    print("Exit")


    # --------------------------------------------------------------------------------------
class Example:
    def __init__(self):
        print("################################################")
        print("Starting robohat test routine")
        self.running = True

        self.robohat = Robohat(main_config.servoassembly_1_config,
                               main_config.servoassembly_2_config,
                               main_config.TOPBOARD_IOEXANDER_SW)

        self.robohat.set_status_system_alarm_permitted(False)

        self.robohat.init(main_config.SERVOBOARD_1_DATAS_ARRAY,
                          main_config.SERVOBOARD_2_DATAS_ARRAY)

    # --------------------------------------------------------------------------------------

    def start_example(self) -> None:
        """!
        Start this example
        @return: None
        """
        print("\n\nWaiting for your input\n\n")

        while self.running is True:
            inp = input()
            self.process_commands(inp)

    # --------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """
        Should stop this program
        @return: None
        """
        print("Exiting this program")
        self.robohat.exit_program()
        self.running = False
        sys.exit(0)

    # --------------------------------------------------------------------------------------

    def set(self, _data_in:str) -> None:
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
                self.robohat.set_servo_angle(servo_nr, angle)
        else:
            print("syntax error")

    # --------------------------------------------------------------------------------------

    def get(self, _data_in:str) -> None:
        """!
        Will handle console request with commando 'get'
        @return: None
        """
        data_in_array = _data_in.split(" ")

        command = data_in_array[1]
        if command == "servo":
            sub_command = data_in_array[2]
            if sub_command == "angle":
                parameter_str:str = data_in_array[3]
                if parameter_str.isnumeric():
                    servo_nr = int(parameter_str)
                    value = self.robohat.get_servo_angle(servo_nr)
                    if value != -1:
                        print("angle of servo " + str(servo_nr) + " is: " + str(value) + "°" )
                elif parameter_str == "all":
                    value = self.robohat.get_servos_angles()
                    print("angles of servos: " + str(value))
                else:
                    print("syntax error")
            elif sub_command == "adc":
                parameter_str: str = data_in_array[3]
                if parameter_str.isnumeric():
                    servo_nr = int(data_in_array[3])
                    value = self.robohat.get_servo_adc_readout_single_channel(servo_nr)
                    if value != -1:
                        print("adc of servo " + str(servo_nr) + " is: " + str(value) + "V" )
                elif parameter_str == "all":
                    value = self.robohat.get_servos_adc_readout_multiple_channels()
                    print("adc volts of servos: " + str(value))
                else:
                    print("syntax error")

    # --------------------------------------------------------------------------------------

    def do(self, _data_in:str) -> None:
        """!
        Will handle console request with commando 'do'
        @return: None
        """
        data_in_array = _data_in.split(" ")

        command = data_in_array[1]
        if command == "i2c":
            sub_command = data_in_array[2]
            if sub_command == "scan":
                self.robohat.scan_i2c_bus()
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
                print("syntax error")
        else:
            print("syntax error")
    # --------------------------------------------------------------------------------------

    def shutdown_power(self) -> None:
        self.robohat.shutdown_power()
    # --------------------------------------------------------------------------------------

    def print_help(self) -> None:
        """
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

        print("do i2c scan                                    scans the i2c bus")
        print("do buzzer random                               generate a random sound")
        print("do buzzer slowwoop                             generate a slowwoop sound")
        print("do buzzer beep                                 generate a beep")
        print("do buzzer freq [frequency]                     generates a sound with requested frequency")
        print("do buzzer stop                                 stop the generation of sound")

    def process_commands(self, _command:str):
        if _command == "exit":
            self.exit_program()

        elif _command == "help":
            self.print_help()

        elif _command == "shutdown":
            self.shutdown_power()

        elif _command.startswith("set"):
            self.set(_command)

        elif _command.startswith("get"):
            self.get(_command)

        elif _command.startswith("do"):
            self.do(_command)

        elif _command.startswith("\n"):
            print("")
        else:
            print("syntax error")


        #print("command: " + _command)
        #self.running = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()


    # #robohat.set_direction_ioexpander(0, EXPANDERDIR.OUTPUT)
    # #robohat.set_direction_ioexpander(1, EXPANDERDIR.OUTPUT)
    #
    # while True:
    #     #adccodesarry = robohat.get_servos_adc_readout_multiple_channels()
    #     #print(adccodesarry)
    #     # for i in range(1,17):
    #     #     #print("-->" + str(i) + " " + str(adccodesarry[i]) + " V")
    #     #
    #     #
    #     #     print(str(i) + "-->" + str(robohat.get_servo_adc_readout_single_channel(i)) + " V, " + str(robohat.get_servo_angle(i)) + " °")
    #     #
    #
    #
    #
    #
    #
    #     #angledarray = robohat.get_servos_angles()
    #     #print(angledarray)
    #     # for i in range(1,17):
    #     #     print("-->" + str(i) + " " + str(angledarray[i]) + " °")
    #     #voltage_adc_hat = robohat.get_readout_hatadc_mutiplechannels()
    #     #print("-->" + str(voltage_adc_hat) + " V")
    #     # robohat.set_servoassembly_1_servo_angle(1, 180)
    #     # time.sleep(1)
    #     #robohat.set_servoassembly_1_servo_angle(1, 0)
    #     # time.sleep(1)
    #     #robohat.set_ouput_ioexpander(0, EXPANDERSTATUS.LOW)
    #     #robohat.set_ouput_ioexpander(1, EXPANDERSTATUS.LOW)
    #
    #     robohat.set_led_color(Color.GREEN)
    #     # for i in range(1,1800, 1):
    #     #     angle:float = i / 10.0
    #     #     robohat.set_servos_angles([angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle])
    #     # # #print("-->" + str(robohat.get_servo_adc_readout_single_channels(1)) + " V," + str(robohat.get_servo_adc_readout_single_channels(16)) + " V")
    #     #     print("-->" + str(robohat.get_servo_angle(1)) + " °," + str(robohat.get_servo_angle(16)) + " °")
    #     #
    #     time.sleep(5)
    #     # robohat.put_servos_to_sleep()
    #     # time.sleep(5)
    #     # robohat.wakeup_servos()
    #     #
    #     robohat.set_led_color(Color.RED)
    #     # for i in range(1800,1, -1):
    #     #     angle:float = i / 10.0
    #     #     robohat.set_servos_angles([angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle])
    #     #     print("-->" + str(robohat.get_servo_angle(1)) + " °" + str(robohat.get_servo_angle(16)) + " °")
    #     #
    #     time.sleep(5)
    #     # robohat.put_servos_to_sleep()
    #     # time.sleep(5)
    #     # robohat.wakeup_servos()
    #
    #     #robohat.do_shutdown()
    #
    #     #print("connected: " + str(robohat.get_is_servo_connected(1)) )
    #
    #     # robohat.set_servoassembly_1_allservos_angle([  70, 0,   0, 0,   0, 180,   0, 180,   0, 180,   0, 180,   0, 180,   0, 180])
    #     # time.sleep(2)
    #     # #print("Stat " + str(robohat.get_input_ioexpander(2)))
    #     # #robohat.set_ouput_ioexpander(0,EXPANDERSTATUS.HIGH)
    #     # #robohat.set_ouput_ioexpander(1, EXPANDERSTATUS.HIGH)
    #     # #
    #     # #
    #     # # adccodesarry = robohat.get_servoassembly_1_readout_adc_mutiplechannels()
    #     # # for i in range(0,16):
    #     # #     print("-->" + str(i) + " " + str(adccodesarry[i]) + " V")
    #     # #
    #     # # robohat.set_color_led(Color.GREEN)
    #     # robohat.set_servoassembly_1_allservos_angle([120,   180, 180,   180, 180,   0, 180,   0, 180,   0, 180,   0, 180,   0, 180,   0])
    #     #
    #
    #     #print("Stat " + str(robohat.get_input_ioexpander(2)) )
    #
    #     #robohat.slowwoop_buzzer()
    #     #robohat.beep_buzzer()
    #
    #     #robohat.do_imu_test()
    #
    #     #print("------------------------------------------------------------")






