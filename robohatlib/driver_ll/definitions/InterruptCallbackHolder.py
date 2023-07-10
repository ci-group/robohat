
try:
    import time
except ImportError:
    print("Failed to import needed dependencies for the InterruptCallbackHolder class")
    raise


class InterruptCallbackHolder:
    def __init__(self, _name:str, _callback = None, _release_int_function = None, _time_between_new_possible_trigger = 0):
        """!
        Constructor of InterruptCallbackHolder
        @param _name:  name of this Holder
        """
        self.__name = _name
        self.__callback = _callback
        self.__release_int_function = _release_int_function
        self.__time_between_new_possible_trigger = 0

        self.set_time_between_new_possible_trigger_in_ms(_time_between_new_possible_trigger);

        self.__last_time_triggered = 0

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------0------------------------------------------------------------------------

    def set_callback(self, _callback) -> None:
        self.__callback = _callback

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def set_release_int_function(self, _release_int_function) -> None:
        self.__release_int_function = _release_int_function

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    def set_time_between_new_possible_trigger_in_ms(self, _time_between_new_possible_trigger) -> None:
        self.__time_between_new_possible_trigger = _time_between_new_possible_trigger * 1000000

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def execute_callback(self, _io_nr:int) -> None:
        if self.__release_int_function is not None:
            self.__release_int_function(_io_nr)

        diff_trigger_time = time.time_ns() - self.__last_time_triggered

        if diff_trigger_time > self.__time_between_new_possible_trigger:
            if self.__callback is not None:
                print("diff: " + str(diff_trigger_time) + " compare: " + str(self.__time_between_new_possible_trigger) )
                self.__last_time_triggered = time.time_ns()
                print("last: " + str(self.__last_time_triggered) )

                self.__callback(_io_nr)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------