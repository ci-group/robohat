#!/usr/bin/python3
try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError("GPIO not found, needed for GP_interrupt class")

try:
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
    from robohatlib.driver_ll.definitions.InterruptCallbackHolder import InterruptCallbackHolder
except ImportError:
    raise ImportError("Unable to solve all dependencies for GPI_LL_Interrupt")

    # --------------------------------------------------------------------------------------

class GPI_LL_Interrupt:
    """!
    Common interrupt driver.
    When fired, will execute callback which are stored in an array
    """

    def __init__(self, _interrupt_definition: GPIInterruptDef):
        """!
        GPI_LL_Interrupt constructor
        @param _interrupt_definition: definition of the interrupt
        """
        self.__name = "common_int"

        if self.__callback_function is None:
            raise Exception("Unable to register interrupt " + self.__name + ", callback is Nome")

        self.__gpio_pin = _interrupt_definition.get_gpio_pin()
        self.__interrupt_type_port = _interrupt_definition.get_interrupt_type_port()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpio_pin, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self.__gpio_pin, GPIO.BOTH, self.__callback_function, 1)

        self.__registered_callbackholders = []
        self.add_callbackholder(_interrupt_definition.get_callbackholder())

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_name(self):
        """!
        Gives name of driver

        @return: str name of driver
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_gpio_pin(self) -> int:
        """!
        Get GPI pin
        @return: gpi pin
        """
        return self.__gpio_pin

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def add_callbackholder(self, _callbackholder: InterruptCallbackHolder) -> None:
        """!
        Add callback
        @param _callbackholder: the callback to be added
        @return: None
        """
        if len(self.__registered_callbackholders) is 0:
            print("first callback")
            self.__registered_callbackholders.append(_callbackholder)

        for callback_out_of_list in self.__registered_callbackholders:
            if callback_out_of_list is _callbackholder:
                print("callback already present")
                return

        print("new callback")
        self.__registered_callbackholders.append(_callbackholder)

    # --------------------------------------------------------------------------------------

    def remove_callbackholder(self, _callbackholder: InterruptCallbackHolder) -> None:
        """!
        Removes callback
        @param _callbackholder removes callback
        @Return None
        """
        if len(self.__registered_callbackholders) is 0:
            return

        for callback_out_of_list in self.__registered_callbackholders:
            self.__registered_callbackholders.remove(callback_out_of_list)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __callback_function(self, _pin_nr) -> None:
        """!
        The actual interrupt callback, which executes all the callback retrieved from a callbackholder stored in an array
        @return: None
        """
        print("callback " + str(_pin_nr))
        if len(self.__registered_callbackholders) is 0:
            return

        for callbackholder_out_of_list in self.__registered_callbackholders:
            print("Execution callback")
            callbackholder_out_of_list.execute_callback(_pin_nr)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


