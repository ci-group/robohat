try:
    from robohatlib.Robohat_config import ALARM_PERMITTED, ALARM_TIMEOUT_IN_SEC, INIT_BEEP_PERMITTED
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

    # init buzzer -------------------------------------------------------------------------------------
    def init_buzzer(self) -> None:
        """
        Initializes the buzzer

        Mandatory

        @return None
        """
        if INIT_BEEP_PERMITTED is True:
            self.__buzzer_driver.init_buzzer(True)
        else:
            self.__buzzer_driver.init_buzzer(False)

    # random buzzer -------------------------------------------------------------------------------------
    def buzzer_random(self) -> None:
        """!
        Generates a random sound

        @return None
        """
        self.__buzzer_driver.random_buzzer()


    # slow woop ----------------------------------------------------------------------------------------
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

    def signal_system_alarm(self) -> None:
        """
        System alarm
        @return: None
        """

        if ALARM_PERMITTED is True:
            diff_time_in_seconds = time.time() - self.__last_time_error
            if diff_time_in_seconds > ALARM_TIMEOUT_IN_SEC:
                self.__buzzer_driver.do_alarm_buzzer()
                print("System alarm")
                self.__last_time_error = time.time()

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------