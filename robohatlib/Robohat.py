from __future__ import annotations

try:
    from robohatlib import Robohat_config
    from robohatlib import Robohat_constants

    from robohatlib.drivers.datastructs.McpInitStruct import McpInitStruct

    from robohatlib.driver_ll.IOHandler import IOHandler
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.constants.GPIO_Direction import GpioDirection
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
    from robohatlib.hal.datastructure.AccuStatus import AccuStatus

    from robohatlib.hal.assemblyboard.ServoAssembly import ServoAssembly
    from robohatlib.hal.HatADC import HatADC
    from robohatlib.hal.assemblyboard.servo.ServoBoard import ServoBoard
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
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

    # --------------------------------------------------------------------------------------
    # constructor Robohat

    def __init__(self, _servo_assembly_1_config: ServoAssemblyConfig, _servo_assembly_2_config: ServoAssemblyConfig, _switch_top_board: int = 7):
        """!
        The Robohat base class initializer.

        Checks if dip switches have no conflict
        Initializes all the IO

        @param _servo_assembly_1_config config of servo assembly 1
        @param _servo_assembly_2_config config of servo assembly 2
        @param _switch_top_board dip-switch settings og the top board (board mounted on RPi), default 7
        """
        print("\n")
        print("Starting Robohat lib: " + Robohat_constants.ROBOHAT_LIB_VERSION_STR + "\n")

        if _switch_top_board is _servo_assembly_1_config.get_sw2_power_good_address() or \
                _switch_top_board is _servo_assembly_2_config.get_sw2_power_good_address() or \
                _servo_assembly_1_config.get_sw2_power_good_address() is _servo_assembly_2_config.get_sw2_power_good_address():
            print("Error, dip-witches in config are in conflict, can't continue.")
            print("Preferred config is, the first assembly board on 0, the second on 1 and the switch on the topboard on 7 ")
            return

        self.__io_handler = IOHandler()
        self.__serial = Serial(self.__io_handler, Robohat_config.SERIAL_DEF)
        self.__buzzer = Buzzer(self.__io_handler, Robohat_config.BUZZER_DEF)
        self.__led = LedMulticolor(self.__io_handler, Robohat_config.STATUS_LED_DEF)
        self.__imu = IMU(self.__io_handler, Robohat_config.IMU_DEF)

        #-------------------------------------Expander
        hat_io_expander_def = Robohat_config.TOPBOARD_IO_EXPANDER_DEF

        # at the default interrupt definition there are 2 callback added. one for the trigger, the second for the interrupt reset
        hat_io_expander_callbackholder = InterruptCallbackHolder("hat_IO_expander_callback_holder",
                                                                 self.__hat_io_expander_int_callback,
                                                                 self.__hat_io_expander_int_reset_routine,
                                                                 InterruptTypes.INT_BOTH,
                                                                 250)

        hat_io_expander_def.set_callbackholder(hat_io_expander_callbackholder)

        self.__hat_io_expander = IOExpander(self.__io_handler, hat_io_expander_def, _switch_top_board)
        self.__hat_adc = HatADC(self.__io_handler, Robohat_config.TOPBOARD_ADC_I2C_DEF)

        self.__power_management = PowerManagement(self.__io_handler,
                                                  self.__hat_adc,
                                                  Robohat_config.POWER_SHUTDOWN_GPO_DEF)

        self.__power_management.add_signaling_device(self.__buzzer)

        self.__servo_assembly_1 = ServoAssembly(self.__io_handler,
                                                _servo_assembly_1_config,
                                                Robohat_config.SERVOASSEMBLY_1_I2C_BUS,
                                                Robohat_config.SERVOASSEMBLY_1_SPI_BUS
                                                )

        if self.__servo_assembly_1 .is_board_avaible() is True:
            self.__servo_assembly_1.add_signaling_device(self.__buzzer)
        else:
            self.__servo_assembly_1 = None              # if not available make None, so class is not accessible

        self.__servo_assembly_2 = ServoAssembly(self.__io_handler,
                                                _servo_assembly_2_config,
                                                Robohat_config.SERVOASSEMBLY_2_I2C_BUS,
                                                Robohat_config.SERVOASSEMBLY_2_SPI_BUS
                                                )

        if self.__servo_assembly_2.is_board_avaible() is True:
            self.__servo_assembly_2.add_signaling_device(self.__buzzer)
        else:
            print("did not fpund board 2")
            self.__servo_assembly_2 = None              # if not available make None, so class is not accessible


        if self.__servo_assembly_1 is None and self.__servo_assembly_2 is None:
            print("Error, no assembly-boards are available")

    # --------------------------------------------------------------------------------------

    def init(self, _servo_board_1_datas_array: [], _servo_board_2_datas_array: []) -> None:
        """!
        Initializes the Robohat

        Mandatory

        @param _servo_board_1_datas_array, servo data array 1
        @param _servo_board_2_datas_array, servo data array 2

        @return None
        """

        self.__io_handler.init_io()
        self.__serial.init_serial()
        self.__buzzer.init_buzzer()
        self.__led.init_led()
        self.__imu.init_imu()
        self.__hat_io_expander.init_io_expander()

        self.__hat_adc.init_hat_adc()
        self.__power_management.init_power_management()

        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.init_servo_assembly(_servo_board_1_datas_array)

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.init_servo_assembly(_servo_board_1_datas_array)

        self.__io_handler.start_interrupts()

    # --------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """
        Exit the program.
        @return: None
        """
        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.exit_program()

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.exit_program()

        self.__serial.exit_program()
        self.__imu.exit_program()
        self.__hat_io_expander.exit_program()
        self.__hat_adc.exit_program()

        self.__led.exit_program()
        self.__buzzer.exit_program()
        self.__power_management.exit_program(False)

        self.__io_handler.exit_program()


    # begin I2C functions ---------------------------------------------------------------------------------
    def do_i2c_scan(self) -> None:
        """!
        Scans all the available I2C busses on the Robohat hardware
        Displays the found I2C devices onto console
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
    def get_assemblyboard_is_connected(self, _assemblyboard: int ) -> bool:
        """!
        Check is an assemblyboard is available. Returns true when available
        @param _assemblyboard: nr of requested assemblyboard. Use Robohat_constants.PWMPLUG_P3 or Robohat_constants.PWMPLUG_P4
        @return: bool
        """

        if _assemblyboard is Robohat_constants.PWMPLUG_P3:
            if self.__servo_assembly_1 is not None:
                return True
        elif _assemblyboard is Robohat_constants.PWMPLUG_P4:
            if self.__servo_assembly_2 is not None:
                return True
        return False

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
                return servo_assembly.get_servo_adc_readout_single_channel(servo_nr)
        return -1
    # --------------------------------------------------------------------------------------

    def get_servo_adc_multiple_channels(self):
        """!
        Get voltages of the potentiometer of all the servos in volt or en empty array
        @return array of voltages
        """

        return_data = []

        if self.__servo_assembly_1 is not None:
            data_assembly1 = self.__servo_assembly_1.get_adc_multiple_channels()
            return_data.append(data_assembly1)

        if self.__servo_assembly_2 is not None:
            data_assembly2 = self.__servo_assembly_2.get_adc_multiple_channels()
            return_data.append(data_assembly2)

        if self.__servo_assembly_1 is not None and self.__servo_assembly_2 is not None:
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

    # ------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------

    def get_servo_multiple_angles(self) -> []:
        """!
        Get an array of the angles of all the servos
        Depending on available assembly, an empty array, array of 16 elements or an array od 32 elements will be returned

        @return angles array
        """

        return_data = []

        if self.__servo_assembly_1 is not None:
            data_assembly1 = self.__servo_assembly_1.get_all_servos_angle()
            return_data.append(data_assembly1)

        if self.__servo_assembly_2 is not None:
            data_assembly2 = self.__servo_assembly_2.get_all_servos_angle()
            return_data.append(data_assembly2)

        return return_data

    # ------------------------------------------------------------------------------------------

    def set_servo_multiple_angles(self, _angles_array: []) -> None:
        """!
        Set the angle of connected servos in degree
        Expect an array of angles. The array should have 16 elements (if only assembly 1 is connected) or array should
        have 32 elements (if both assemblies are connected)

        @param _angles_array, array of the angles
        @return None
        """

        if self.__servo_assembly_1 is not None:
            angles_array1 = _angles_array[0:16]
            self.__servo_assembly_1.set_servo_multiple_angles(angles_array1)

        if self.__servo_assembly_2 is not None and len(_angles_array) >= 32:
            angles_array2 = _angles_array[16:32]
            self.__servo_assembly_2.set_servo_multiple_angles(angles_array2)

        # ------------------------------------------------------------------------------------------
    def put_servo_to_sleep(self) -> None:
        """!
        Puts servos to sleep. Note servos will be powered down
        @return: None
        """

        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.sleep()

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.sleep()

    # ------------------------------------------------------------------------------------------

    def wakeup_servo(self) -> None:
        """!
        Wakes up the servos
        @return: None
        """

        if self.__servo_assembly_1 is not None:
            self.__servo_assembly_1.wake()

        if self.__servo_assembly_2 is not None:
            self.__servo_assembly_2.wake()

    # ------------------------------------------------------------------------------------------

    def is_servo_sleeping(self) -> bool:
        """
        Get if Servos are sleeping
        @return: True when servos are sleeping
        """

        if self.__servo_assembly_1 is not None:
            return self.__servo_assembly_1.is_servo_sleeping()

        elif self.__servo_assembly_2 is not None:
            return self.__servo_assembly_2.is_servo_sleeping()

        return True

    # ------------------------------------------------------------------------------------------

    def set_servo_io_expander_direction(self, _board_nr: int, _pin_nr: int, _dir: ExpanderDir) -> None:
        """!
        Set the direction of the IO pin on a servo board.
        @param _board_nr: board nr
        @param _pin_nr:  pin nr
        @param _dir: on or out
        @return None:
        """

        if _board_nr == Robohat_constants.PWMPLUG_P3:               # board 0
            if self.__servo_assembly_1 is not None:
                self.__servo_assembly_1.set_servo_io_expander_direction(_pin_nr, _dir)
            else:
                print("Error: servo assembly 1 not initialized")
        elif _board_nr == Robohat_constants.PWMPLUG_P4:             # board 1
            if self.__servo_assembly_2 is not None:
                self.__servo_assembly_2.set_servo_io_expander_direction(_pin_nr, _dir)
            else:
                print("Error: servo assembly 2 not initialized")
        else:
            print("Error: servo assembly 1 and servo assembly 2 are not initialized")

    # ------------------------------------------------------------------------------------------

    def get_servo_io_expander_direction(self, _board_nr: int, _pin_nr: int) -> ExpanderDir | None:
        """!
        Set the direction of the IO pin on a servo board.
        @param _board_nr: board nr
        @param _pin_nr:  pin nr
        @return ExpanderDir:
        """

        if _board_nr == Robohat_constants.PWMPLUG_P3:               # board 0
            if self.__servo_assembly_1 is not None:
                return self.__servo_assembly_1.get_servo_io_expander_direction(_pin_nr)
            else:
                print("Error: servo assembly 1 not initialized")
                return None
        elif _board_nr == Robohat_constants.PWMPLUG_P4:             # board 1
            if self.__servo_assembly_2 is not None:
                return self.__servo_assembly_2.get_servo_io_expander_direction(_pin_nr)
            else:
                print("Error: servo assembly 2 not initialized")
                return None
        else:
            print("Error: servo assembly 1 and servo assembly 2 are not initialized")
        return None

    # ------------------------------------------------------------------------------------------

    def set_servo_io_expander_output(self, _board_nr: int, _pin_nr: int, _value: ExpanderStatus) -> None:
        """!
        Set the value of the IO pin on a servo board. Note, io pin should be an output
        @param _board_nr: board nr
        @param _pin_nr:  pin nr
        @param _value: low or high
        @return None:
        """
        if _board_nr == Robohat_constants.PWMPLUG_P3:               # board 0
            if self.__servo_assembly_1 is not None:
                self.__servo_assembly_1.set_servo_io_expander_output(_pin_nr, _value)
            else:
                print("Error: servo assembly 1 not initialized")
        elif _board_nr == Robohat_constants.PWMPLUG_P4:             # board 1
            if self.__servo_assembly_2 is not None:
                self.__servo_assembly_2.set_servo_io_expander_output(_pin_nr, _value)
            else:
                print("Error: servo assembly 2 not initialized")
        else:
            print("Error: servo assembly 1 and servo assembly 2 are not initialized")
    # ------------------------------------------------------------------------------------------

    def get_servo_io_expander_input(self, _board_nr: int, _pin_nr: int) -> ExpanderStatus | None:
        """!
        Get the value of the IO pin on a servo board. Note, io pin should be an output
        @param _board_nr: board nr
        @param _pin_nr:  pin nr
        @return None:
        """
        if _board_nr == Robohat_constants.PWMPLUG_P3:               # board 0
            if self.__servo_assembly_1 is not None:
                return self.__servo_assembly_1.get_servo_io_expander_input(_pin_nr)
            else:
                print("Error: servo assembly 1 not initialized")
                return None
        elif _board_nr == Robohat_constants.PWMPLUG_P4:             # board 1
            if self.__servo_assembly_2 is not None:
                return self.__servo_assembly_2.get_servo_io_expander_input(_pin_nr)
            else:
                print("Error: servo assembly 2 not initialized")
                return None
        else:
            print("Error: servo assembly 1 and servo assembly 2 are not initialized")
        return None

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

    # begin HAT ADC functions --------------------------------------------------------------------------------------
    def get_hat_adc_single_channel(self, _channel_nr: int) -> float:
        """!
        Get analog value of a channel from the HAT adc
        Requested channels can be 0 - 3 (channel 4 is the derivative of the accu voltage)

        @param _channel_nr Wanted channel nr. (Starts at 0)
        @return analog voltage
        """

        return self.__hat_adc.get_adc_single_channel(_channel_nr)

    # ------------------------------------------------------------------------------------------

    def get_hat_adc_multiple_channels(self) -> []:
        """!
        Get analog values of the HAT adc
        Returns an array of 4 elements

        @return analog voltage in an array
        """
        return self.__hat_adc.get_adc_multiple_channels()

    # end HAT ADC functions --------------------------------------------------------------------------------------

    # begin IO_EXPANDER functions ---------------------------------------------------------------------------------
    def set_hat_io_expander_direction(self, _io_nr:int, _direction: ExpanderDir) -> None:
        """!
        Set the direction of an io pin of the IO expander

        @param _io_nr io nr
        @param _direction the direction of the pin.

        @return None
        """

        self.__hat_io_expander.set_direction_io_expander(_io_nr, _direction)

    def get_hat_io_expander_direction(self, _io_nr:int) -> ExpanderDir:
        """!
        Get the direction of an io pin of the IO expander

        @param _io_nr io nr

        @return ExpanderDir
        """

        return self.__hat_io_expander.get_direction_io_expander(_io_nr)


    def set_hat_io_expander_output(self, _io_nr: int, _status: ExpanderStatus) -> None:
        """!
        Set the output status of an io pin of the IO expander

        Note. direction of the pin must be an Output

        @param _io_nr io nr
        @param _status the status o the pin

        @return None
        """
        self.__hat_io_expander.set_io_expander_output_status(_io_nr, _status)

    def get_hat_io_expander_input(self, _io_nr):
        """!
        get the input status of an io pin of the IO expander

        Note. direction of the pin must be an Input

        @param _io_nr io nr

        @return status of the pin
        """
        return self.__hat_io_expander.get_io_expander_input(_io_nr)

    # end IO_EXPANDER functions ------------------------------------------------------------------------------------
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
    def get_accu_percentage_capacity(self) -> int:
        """!
        Get capacity of accu in percentage

        @return: percentage
        """
        return self.__power_management.get_accu_percentage_capacity()

    def get_accu_voltage(self) -> float:
        """!
        Get voltage of accu

        @return: voltage of accu
        """

        return self.__power_management.get_accu_voltage()

    def get_accu_status(self) -> AccuStatus:
        """!
        Returns True if accu capacity is OK

        @return True is accu capacity is OK
        """
        return self.__power_management.get_accu_status()

    # end Power management functions -------------------------------------------------------------------------
    # begin System functions ---------------------------------------------------------------------------------

    def do_system_shutdown(self) -> None:
        """!
        Sends shutdown signal to power module, cleans-up IO, shutdowns the RPi
        @return None
        """

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

        return Robohat_constants.ROBOHAT_LIB_VERSION_STR

    # ------------------------------------------------------------------------------------
    # noinspection PyMethodMayBeStatic
    def get_lib_build_date(self) -> str:
        """!
        Get the build date of library.

        @return str, version build date of library, such as 20231225
        """
        return Robohat_constants.ROBOHAT_BUILD_DATE_STR

    # End Library functions ---------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------

    # some test routines
    def __hat_io_expander_int_callback(self, _gpi_nr: int) -> None:
        """!
        Just a test callback, for the hat_io_expander

        @param _gpi_nr (int) mr of the callback gpio pin
        @return None
        """
        #print("hat__io_expander_int_callback by: " + str(_gpi_nr))
        self.do_buzzer_beep()

    def __hat_io_expander_int_reset_routine(self, _gpi_nr: int) -> None:
        """!
        This routine will be called to reset the interrupt handler (if needed, is used by MCP23008)
        @param _gpi_nr: IO nr of the caller
        @return: None
        """
        if self.__hat_io_expander is not None:
            self.__hat_io_expander.reset_interrupt(_gpi_nr)

    # ------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------



