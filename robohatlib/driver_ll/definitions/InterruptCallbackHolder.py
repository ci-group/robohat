"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""


try:
    import time
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
except ImportError:
    print("Failed to import needed dependencies for the InterruptCallbackHolder class")
    raise


class InterruptCallbackHolder:
    def __init__(self, _name:str, _callback = None, _release_int_function = None, _interrupt_type:InterruptTypes = InterruptTypes.INT_BOTH, _time_between_new_possible_trigger = 0):
        """!
        Constructor of InterruptCallbackHolder

        @param _name: name of this Holder
        @param _callback: Function which will be called when the trigger is executed
        @aram _release_int_function: Function which will be called after the callback function is executed
        @param _interrupt_type: Type of interrupt (Falling, Rising, Both)
        @param _time_between_new_possible_trigger:  Time out between triggers in mS
        """

        self.__name = _name
        self.__callback = _callback
        self.__release_int_function = _release_int_function
        self.__interrupt_type = _interrupt_type
        self.__time_between_new_possible_trigger = 0

        self.set_time_between_new_possible_trigger_in_ms(_time_between_new_possible_trigger)

        self.__last_time_triggered = 0

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------0------------------------------------------------------------------------

    def set_callback_function(self, _callback) -> None:
        """!
        A new function which will be called when the trigger is executed

        @param _callback: a new function
        @return: Nome
        """
        self.__callback = _callback

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def set_release_int_release_function(self, _release_int_function) -> None:
        """
        A new function which will be called when the trigger is executed

        @param _release_int_function: a new function
        @return: None
        """
        self.__release_int_function = _release_int_function

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def set_time_between_new_possible_trigger_in_ms(self, _time_between_new_possible_trigger:int = 0) -> None:
        """!
        The minimal time between 2 triggers. 0 = default

        @param _time_between_new_possible_trigger:
        @return: None
        """
        self.__time_between_new_possible_trigger = _time_between_new_possible_trigger * 1000000

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def execute_callback(self, _io_nr:int) -> None:
        """!
        This function will call the 'reset the interrupt function' and the and executes 'callback function'

        @param _io_nr: io nr which triggered the interrupt
        @return: None
        """

        diff_trigger_time = time.time_ns() - self.__last_time_triggered
        if diff_trigger_time > self.__time_between_new_possible_trigger:
            if self.__callback is not None:
                self.__last_time_triggered = time.time_ns()
                self.__callback(_io_nr)

        # release have to be done, when interrupt is handled. Otherwise, no data can be read
        if self.__release_int_function is not None:
            self.__release_int_function(_io_nr)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def  get_interrupt_type(self) -> InterruptTypes:
        """!
        Returns wanted interrupt type

        @return InterruptTypes
        """
        return  self.__interrupt_type