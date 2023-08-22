"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    import RPi.GPIO as GPIO
    from robohatlib.driver_ll.definitions.GPOPWMDef import GPOPWMDef
    from time import sleep
    import random

except ImportError:
    raise ImportError("Dependencies not found, needed for GPOPWM_LL_Driver class")


class GPOPWM_LL_Driver:
    """
    Driver of a GPIO output configured as PWM
    """

    def __init__(self, _gpo_pwm_definition:GPOPWMDef):
        """!
        @param _gpo_pwm_definition: definition for the PWM
        """
        self._gpo_pwm_definition = _gpo_pwm_definition

        self.__freq = _gpo_pwm_definition.get_freq()
        self.__dutycylce = _gpo_pwm_definition.get_duty_cycle()
        self.__name = _gpo_pwm_definition.get_name()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(_gpo_pwm_definition.get_gpo_pin_nr(), GPIO.OUT)

        self.__pwm = GPIO.PWM(_gpo_pwm_definition.get_gpo_pin_nr(), self.__freq)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_pwm(self, _freq: int, _duty_cycle: int, _sleep_time: int) -> None:
        """!
        PWM for while, depending on the sleep time

        @param _freq start frequency
        @param _duty_cycle stop frequency
        @param _sleep_time step size. (Should be positive)

        @return None
        """

        self.allocate(50)

        self.set_freq(_freq)
        sleep(_sleep_time)

        self.release()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_random_freq(self) -> None:
        """!
        Do a random PWM

        @return None
        """

        self.allocate(50)

        for loop in range(0, 20, 1):
            self.set_freq(random.randint(50, 1000))
            self.set_dutycycle(50)
            sleep(0.05)
            self.set_dutycycle(0)
            sleep(0.05)

        self.release()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_ramp_freq(self, _start_freq: int, _stop_freq: int, _step_size: int) -> None:
        """!
        Ramp PWM

        @param _start_freq start frequency
        @param _stop_freq stop frequency
        @param _step_size step size. (Should be positive)

        @return None
        """

        if _step_size < 0:
            raise Exception("step size below 0")

        step_size = _step_size
        if _start_freq > _stop_freq:
            step_size = _step_size * -1

        self.allocate(50)

        for buzz_freq in range(_start_freq, _stop_freq, step_size):
            self.set_freq(buzz_freq)
            sleep(0.005)

        self.release()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def do_single_freq(self, _freq: int) -> None:
        """!
        PWM at a requested frequency. Has to be released when finished

        @param _freq start frequency

        @return None
        """

        self.allocate(50)
        self.set_freq(_freq)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_dutycycle(self, _dutycylce: int) -> None:
        """!
        Sets duty cycle

        @param _dutycylce wanted duty cycle

        @return None
        """
        self.__pwm.ChangeDutyCycle(_dutycylce)
        self.__dutycylce = _dutycylce

    # --------------------------------------------------------------------------------------

    def get_dutycycle(self) -> int:
        """!
        Get current duty cycle

        @return duty cycle
        """
        return self.__dutycylce

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_freq(self, _freq: int) -> None:
        """!
        Set currents frequency

        @param _freq: frequency in Hz
        @return: None
        """

        self.__pwm.ChangeFrequency(_freq)
        self.__freq = _freq

    # --------------------------------------------------------------------------------------

    def get_freq(self) -> int:
        """!
        Gives current frequency

        @return: frequency
        """

        return self.__freq

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Gives name of driver

        @return: str name of driver
        """

        return self.__name

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def allocate(self, _duty_cycle: int) -> None:
        """
        Starts PWM

        @param _duty_cycle initial duty cycle
        @return: None
        """
        self._start()
        self.set_dutycycle(_duty_cycle)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def release(self) -> None:
        """!
        Releases PWM

        @return: None
        """

        self.__pwm.ChangeFrequency(1000)
        self.__pwm.ChangeDutyCycle(0)
        self._stop()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


    def _start(self) -> None:
        """!
        Starts the PWM generation, dutycycle 0

        @return: Nome
        """

        self.__pwm.start(0)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _stop(self) -> None:
        """!
        Stops the PWM generation
        @return: Nome
        """

        self.__pwm.stop()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
