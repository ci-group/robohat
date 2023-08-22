"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    import RPi.GPIO as GPIO
    from robohatlib.driver_ll.constants.GPOStat import GPOStat
    from robohatlib.driver_ll.definitions.GPODef import GPODef
except ImportError:
    raise ImportError("GPIO not found, needed for GPO_LL_Driver class")


class GPO_LL_Driver:
    """
    Driver of a GPIO output
    """

    def __init__(self, _gpo_definition:GPODef):
        """
        Constructor
        @param _gpo_definition: definition of this output pin
        """
        self.__gpo_definition = _gpo_definition
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpo_definition.get_gpo_pin_nr(), GPIO.OUT)
        self.__status = GPOStat.GPO_LOW
        self.set_low()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_low(self) -> None:
        """!
        Set output to low

        @return: None
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpo_definition.get_gpo_pin_nr(), GPIO.OUT)
        GPIO.output(self.__gpo_definition.get_gpo_pin_nr(), GPIO.LOW)
        self.__status = GPOStat.GPO_LOW

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_high(self) -> None:
        """!
        Set output to high

        @return: None
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpo_definition.get_gpo_pin_nr(), GPIO.OUT)
        GPIO.output(self.__gpo_definition.get_gpo_pin_nr(), GPIO.HIGH)
        self.__status = GPOStat.GPO_HIGH

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_status(self, _stat) -> None:
        """!
        Set status depending parameter

        @stat status

        @return: None
        """

        if _stat is GPOStat.GPO_LOW:
            self.set_low()
        else:
            self.set_high()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_status(self) -> GPOStat:
        """!
        Give current status

        @return: GPOStat
        """

        return self.__status

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Gives name of driver

        @return: str name of driver
        """

        return self.__gpo_definition.get_name()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


