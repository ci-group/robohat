"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Driver for a buzzer

Needed is the connected PWM_LL_DRIVER
"""

try:
    from time import sleep
except ImportError:
    raise ImportError("Failed to import needed dependencies for the Buzzer_driver class")


class BuzzerDriver:
    def __init__(self, _pwm_ll_driver):
        self.__pwm_ll_driver = _pwm_ll_driver

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def init_buzzer(self, _init_beep_permitted) -> None:
        """!
        Init the buzzer,

        @param _init_beep_permitted: bool, if True, a small beep will sound after init
        @return: None
        """
        if _init_beep_permitted is True:
            self.do_buzzer_beep()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def random_buzzer(self) -> None:
        """!
        Generates a random sound

        @return None
        """
        self.__pwm_ll_driver.do_random_freq()

    #--------------------------------------------------------------------------------------
    def do_buzzer_slowwoop(self) -> None:
        """!
        Generates a sound from 2000Hz to 50Hz

        @return None
        """

        self.__pwm_ll_driver.do_ramp_freq(2000, 50, 4)

    # beep ----------------------------------------------------------------------------------------
    def do_buzzer_beep(self) -> None:
        """!
        Short beep of the buzzer

        @return None
        """
        self.__pwm_ll_driver.do_pwm(1000, 50, 0.100)

    #--------------------------------------------------------------------------------------
    def do_buzzer_freq(self, _beep_freq: int) -> None:
        """!
         Beeps the buzzer at a requested frequency, has to be released or set to 0

         @param _beep_freq wanted frequency in Hz
         @return None
         """
        if _beep_freq == 0:
            self.buzzer_release()
        else:
            self.__pwm_ll_driver.do_single_freq(_beep_freq)

    #--------------------------------------------------------------------------------------

    def do_alarm_buzzer(self) -> None:
        for x in range(0, 3):
            self.do_buzzer_freq(500)
            sleep(.250)
            self.do_buzzer_freq(1000)
            sleep(.250)

        self.__pwm_ll_driver.release()

    #--------------------------------------------------------------------------------------

    def buzzer_release(self) -> None:
        """!
        Releases buzzer

        @return: none
        """
        self.__pwm_ll_driver.release()

    # --------------------------------------------------------------------------------------
