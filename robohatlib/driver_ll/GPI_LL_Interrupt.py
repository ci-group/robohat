#!/usr/bin/python3
try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError("GPIO not found, needed for GP_interrupt class")

try:
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
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

        self.__registered_callbacks = []
        self.add_callback(_interrupt_definition.get_callback_function())

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

    def add_callback(self, _callback) -> None:
        """!
        Add callback
        @param _callback: the callback to be added
        @return: None
        """
        if len(self.__registered_callbacks) is 0:
            print("first callback")
            self.__registered_callbacks.append(_callback)

        for callback_out_of_list in self.__registered_callbacks:
            if callback_out_of_list is _callback:
                print("callback already present")
                return

        print("new callback")
        self.__registered_callbacks.append(_callback)

    # --------------------------------------------------------------------------------------

    def remove_callback(self, _callback) -> None:
        """
        Removes callback
        @param _callback removes callback
        @Return None
        """
        if len(self.__registered_callbacks) is 0:
            return

        for callback_out_of_list in self.__registered_callbacks:
            self.__registered_callbacks.remove(callback_out_of_list)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __callback_function(self) -> None:
        """!
        The actual interrupt callback, which executes all the callback stored in an array
        @return: None
        """
        print("callback")
        if len(self.__registered_callbacks) is 0:
            return

        for callback_out_of_list in self.__registered_callbacks:
            print("Execution callback")
            callback_out_of_list()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


