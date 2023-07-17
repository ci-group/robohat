
from robohatlib.driver_ll.constants.GPO_Stat import GPOStat


class LedDriver:
    def __init__(self,  _gpo_ll_driver):
        self.__gpo_ll_driver = _gpo_ll_driver
        self.__color_active = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def init_led(self):
        #print("init LED")
        self.__color_active = False
        self.__set_status_led_to_vars()
        self.turn_led_off()

    # --------------------------------------------------------------------------------------

    def set_status_led(self, _stat) -> None:            # set state led
        """!
         Sets the status of the LED

         @param _stat True or False

         @return None
         """

        if _stat is True:
            self.__color_active = True
        else:
            self.__color_active = False

        self.__set_status_led_to_vars()

    # --------------------------------------------------------------------------------------

    def turn_led_on(self) -> None:                      # depending on last state
        """!
        Turns led on, with last known color. default color is WHITE

        @return None
        """
        self.__set_status_led_to_vars()

    # --------------------------------------------------------------------------------------
    def turn_led_off(self) -> None:
        """!
        Turns led off, last color will be stored
        @return None
        """
        self.__gpo_ll_driver.set_low()

    # --------------------------------------------------------------------------------------
    def __set_status_led_to_vars(self):
        self.__gpo_ll_driver.set_status(self.__return_gpioval_depending_boolean(self.__color_active))

    # --------------------------------------------------------------------------------------
    # noinspection PyMethodMayBeStatic
    def __return_gpioval_depending_boolean(self, _booleanval):
        if _booleanval is False:
            return GPOStat.GPO_LOW
        else:
            return GPOStat.GPO_HIGH



