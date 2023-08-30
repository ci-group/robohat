"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

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
    When fired, will execute callback which are stored in a list
    """

    def __init__(self, _interrupt_definition: GPIInterruptDef):
        """!
        GPI_LL_Interrupt constructor
        @param _interrupt_definition: definition of the interrupt
        """
        self.__name = "int" + _interrupt_definition.get_name()
        self.__interrupt_definition = _interrupt_definition

        if self.__callback_function is None:
            raise Exception("Unable to register interrupt " + self.__name + ", callback is Nome")

        self.__gpio_pin = _interrupt_definition.get_gpio_pin()
        self.__interrupt_type_port = _interrupt_definition.get_interrupt_type_port()

        self.__registered_callback_holders = []

        self.__int_is_active = False
        self.set_event_detection()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_event_detection(self) -> None:
        """!
        turns on the event detection
        @return: None
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpio_pin, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self.__gpio_pin, GPIO.BOTH, self.__callback_function, 1)

        self.add_callbackholder(self.__interrupt_definition.get_callbackholder())
        #self.int_is_active = True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def remove_event_detection(self) -> None:
        """!
        turns off the event detection
        @return: None
        """
        if self.__int_is_active is True:
            GPIO.remove_event_detect(self.__gpio_pin)
            self.__int_is_active = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start(self) -> None:
        """!
        Starts the interrupt
        @return: None
        """

        self.__int_is_active = True

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
        if len(self.__registered_callback_holders) == 0:
            self.__registered_callback_holders.append(_callbackholder)
            return

        for callback_out_of_list in self.__registered_callback_holders:
            if callback_out_of_list is _callbackholder:
                return

        self.__registered_callback_holders.append(_callbackholder)

    # --------------------------------------------------------------------------------------

    def remove_callbackholder(self, _callbackholder: InterruptCallbackHolder) -> None:
        """!
        Removes callback
        @param _callbackholder removes callback
        @Return None
        """
        if len(self.__registered_callback_holders) == 0:
            return

        for callback_out_of_list in self.__registered_callback_holders:
            self.__registered_callback_holders.remove(callback_out_of_list)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __callback_function(self, _pin_nr) -> None:
        """!
        The actual interrupt callback, which executes all the callback retrieved from a callbackholder stored in a list
        @return: None
        """
        if len(self.__registered_callback_holders) == 0:
            return

        for callbackholder_out_of_list in self.__registered_callback_holders:
            if self.__int_is_active is True:
                callbackholder_out_of_list.execute_callback(_pin_nr)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


