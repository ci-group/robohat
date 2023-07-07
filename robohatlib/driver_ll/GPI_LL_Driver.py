
try:
    import RPi.GPIO as GPIO
    from robohatlib.driver_ll.definitions.GPIDef import GPIDef
except ImportError:
    raise ImportError("GPIO not found, needed for GPI_LL_Driver")


class GPI_LL_Driver:

    def __init__(self, _gpi_definition:GPIDef):
        self.__gpi_definition = _gpi_definition

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpi_definition.get_gpi_pin_nr(), GPIO.IN)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_status(self):
        return GPIO.input(self.__gpi_definition.get_gpi_pin_nr())

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Get nam of this driver
        @return: name
        """
        return self.__gpi_definition.get_name()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


