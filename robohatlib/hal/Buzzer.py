"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.RobohatConfig import ALARM_PERMITTED, ALARM_TIMEOUT_IN_SEC, INIT_BEEP_PERMITTED
    from robohatlib.hal.definitions.BuzzerDef import BuzzerDef
    from robohatlib.driver_ll.IOHandler import IOHandler
    import time
except ImportError:
    raise ImportError("Failed to import needed dependencies for the Buzzer class")

class Buzzer:
    """!
    Buzzer device
    """

    def __init__(self, _io_handler: IOHandler, _buzzer_def:BuzzerDef) -> None:
        """!
        @param _io_handler:
        @param _buzzer_def: configuration of the Buzzer. such as: Buzzer_Definition("buzzer1", 18, 1000, 50), See class Buzzer_Definition

        @return: none
        """
        self.__buzzer_driver = _io_handler.get_buzzer_driver(_buzzer_def)
        self.__last_time_error = 0
        self.__state_alarm_permitted = ALARM_PERMITTED

        # init buzzer -------------------------------------------------------------------------------------
    def init_buzzer(self) -> None:
        """
        Initializes the buzzer

        Mandatory

        @return None
        """

        self.__buzzer_driver.init_buzzer(True)

    # --------------------------------------------------------------------------------------
    def exit_program(self) -> None:
        """
        Cleans up, when user want to shut down
        @return: None
        """
        self.buzzer_beep()

    # random buzzer -------------------------------------------------------------------------------------
    def buzzer_random(self) -> None:
        """!
        Generates a random sound

        @return None
        """
        self.__buzzer_driver.random_buzzer()


    # slowwoop ----------------------------------------------------------------------------------------
    def buzzer_slowwoop(self) -> None:
        """!
        Generates a sound from 2000Hz to 50Hz

        @return None
        """

        self.__buzzer_driver.do_buzzer_slowwoop()

    # beep ----------------------------------------------------------------------------------------
    def buzzer_beep(self) -> None:
        """!
        Short beep of the buzzer

        @return None
        """
        self.__buzzer_driver.do_buzzer_beep()

    # beep ----------------------------------------------------------------------------------------
    def buzzer_freq(self, _freq) -> None:
        """!
         Beeps the buzzer at a requested frequency

         @param _freq wanted frequency in Hz
         @return None
         """
        self.__buzzer_driver.do_buzzer_freq(_freq)

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------
    def buzzer_release(self) -> None:
        """!
        Stops the buzzer from making sound
        @return: None
        """
        self.__buzzer_driver.buzzer_release()

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------

    def set_status_system_alarm_permitted(self, _state:bool) -> None:
        """!
        Overrides the system alarm switch. If false, no sound alarm will be given
        @param _state: new state of system alarm
        @return: None
        """

        print("Override if system alarm is permitted with: " + str(_state))
        self.__state_alarm_permitted = _state

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------

    def get_status_system_alarm_permitted(self) -> bool:
        """!
        Get the system alarm switch. If false, no sound alarm will be given
        @return: None
        """
        return self.__state_alarm_permitted

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------

    def signal_system_alarm(self, _txt:str = None) -> None:
        """
        Sounds a system alarm when permitted. Prints a console Warning
        @return: None
        """

        if self.__state_alarm_permitted is True:
            diff_time_in_seconds = time.time() - self.__last_time_error
            if diff_time_in_seconds > ALARM_TIMEOUT_IN_SEC:
                self.__buzzer_driver.do_alarm_buzzer()
                print("WARNING: System alarm !!!")
                if _txt is not None:
                    print(_txt)
                self.__last_time_error = time.time()
        else:
            print("\nWARNING: System alarm !!!, sound is disabled\n")
            if _txt is not None:
                print(_txt)

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------