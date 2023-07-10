try:
    from robohatlib.hal.datastructure.Color import Color
    from robohatlib.driver_ll.IOHandler import IOHandler
except ImportError:
    raise ImportError("Failed to import needed dependencies for the LedMulticolor class")

class LedMulticolor:

    def __init__(self, _io_handler: IOHandler, _multi_colorled_def):
        """!
        Top class of LedMulticolor.
        This is driver for a multi-color led
        """
        self.__multi_colorled_def = _multi_colorled_def

        self.__led_driver_red = _io_handler.get_led_driver(_multi_colorled_def.get_red_def())
        self.__led_driver_green = _io_handler.get_led_driver(_multi_colorled_def.get_green_def())
        self.__led_driver_blue = _io_handler.get_led_driver(_multi_colorled_def.get_blue_def())

    # --------------------------------------------------------------------------------------
    def init_led(self) -> None:
        """!
        Initializes the LedMulticolor class.

        Mandatory

        @return None
        """

        self.__led_driver_red.init_led()
        self.__led_driver_green.init_led()
        self.__led_driver_blue.init_led()

        self.set_led_color(Color.WHITE)

    # --------------------------------------------------------------------------------------
    def set_led_color(self, _color: Color):
        """!
         Sets the color of the LED and turns the LED on

         @param _color Color of the LED

         @return None
         """

        if _color is Color.NONE:
            self.__led_driver_red.set_status_led(False)
            self.__led_driver_green.set_status_led(False)
            self.__led_driver_blue.set_status_led(False)
        elif _color is Color.WHITE:
            self.__led_driver_red.set_status_led(True)
            self.__led_driver_green.set_status_led(True)
            self.__led_driver_blue.set_status_led(True)
        elif _color is Color.RED:
            self.__led_driver_red.set_status_led(True)
            self.__led_driver_green.set_status_led(False)
            self.__led_driver_blue.set_status_led(False)
        elif _color is Color.GREEN:
            self.__led_driver_red.set_status_led(False)
            self.__led_driver_green.set_status_led(True)
            self.__led_driver_blue.set_status_led(False)
        elif _color is Color.BLUE:
            self.__led_driver_red.set_status_led(False)
            self.__led_driver_green.set_status_led(False)
            self.__led_driver_blue.set_status_led(True)


    # --------------------------------------------------------------------------------------
    def turn_led_on(self) -> None:
        """!
        Turns led on, with last known color. default color is WHITE
        @return None
        """
        self.__led_driver_red.turn_led_on()
        self.__led_driver_green.turn_led_on()
        self.__led_driver_blue.turn_led_on()

    # --------------------------------------------------------------------------------------
    def turn_led_off(self) -> None:
        """!
        Turns led off, last color will be stored
        @return None
        """
        self.__led_driver_red.turn_led_off()
        self.__led_driver_green.turn_led_off()
        self.__led_driver_blue.turn_led_off()
    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Gives name of the LedMulticolor class
        @return None
        """
        return self.__multi_colorled_def.get_name()

    # --------------------------------------------------------------------------------------