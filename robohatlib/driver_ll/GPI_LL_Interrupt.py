
try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError("GPIO not found, needed for GP_interrupt class")

try:
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef
except ImportError:
    raise ImportError("Unable to solve all dependencies for GP_interrupt")


class GP_interrupt:

    def __init__(self, _interruptdefinition:GPIInterruptDef):
        self.__name = _interruptdefinition.get_name()
        self.__callback_function = _interruptdefinition.get_callback_function()

        if self.__callback_function is None:
            raise Exception("Unable to register interrupt " + self.__name + ", callback is Nome")
            return

        self.__gpio_pin = _interruptdefinition.get_gpio_pin()
        #self.__interrupt_type_port = _interruptdefinition.get_interrupt_type_port()


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpio_pin, GPIO.IN, GPIO.PUD_UP)

        if _interruptdefinition.get_interrupt_type_port() is InterruptTypes.INT_FALLING:
            GPIO.add_event_detect(self.__gpio_pin, GPIO.FALLING , self.__callback_function, 1)
        elif _interruptdefinition.get_interrupt_type_port() is InterruptTypes.INT_RISING:
             GPIO.add_event_detect(self.__gpio_pin, GPIO.RISING, self.__callback_function, 1)
        else:
             GPIO.add_event_detect(self.__gpio_pin, GPIO.BOTH, self.__callback_function, 1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_name(self):
        """!
        Gives name of driver

        @return: str name of driver
        """
        return self.__name

    def get_gpio_pin(self):
        return self.__gpio_pin

    def get_interrupt_type_port(self):
        return InterruptTypes.INT_BOTH    #self.__interrupt_type_port

    def get_callbackfunction(self):
        return self.__callback_function

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


