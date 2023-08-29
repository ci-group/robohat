"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

from __future__ import annotations

try:
    import time, threading
    from robohatlib.helpers.RoboUtil import RoboUtil
    from robohatlib.hal.assemblyboard import PowerMonitorAndIO
    from robohatlib.drivers.MCP23008 import MCP23008
    from robohatlib import RobohatConfig

except ImportError:
    print("Failed to import dependencies for PowerMonitorHolder")
    raise

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

class PowerMonitorTimer:
    """!
    This class will monitor if a short still occurs onto the pin which caused the interrupt. If so longer than the time window, send a message to the user
    """

    def __init__(self, _id:int, _mother:PowerMonitorAndIO, _expander:MCP23008):
        """!
        Constructor of this dataholder
        @param _id: id of this class
        """
        self.__id = _id
        self.__mother = _mother
        self.__expander = _expander

        self.__busy = False

    #--------------------------------------------------------------------------------------

    def get_id(self) -> int:
        """!
        Returns ID of this dataholder
        @return:
        """
        return self.__id

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def task(self):
        """!
        Our running task which is a separate thread
        @return: None

        Will trigger the alarm when the I/O stays low in the time-window
        """

        self.__busy = True
        start_time = RoboUtil.get_time_ms()

        while self.__busy:
            current_time = RoboUtil.get_time_ms()
            diff_time = current_time - start_time

            if self.__expander.get_pin_data(self.__id) == 1:        # pin when high, so no short anymore. is in the threshold. so no alarm, get out of this loop
                self.__busy = False
            else:
                if diff_time >= RobohatConfig.TIME_WINDOW_TO_BE_DCDC_SHORT_TO_ALARM:
                    self.__busy = False
                    self.__trigger_error()

            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_is_busy(self) -> bool:
        """!
        Return True when the task is Running
        @return: bool
        """
        return self.__busy

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __trigger_error(self) -> None:
        """!
        Will trigger an error message to the user
        @return: Nome
        """
        print("Major error: power fail DC/DC " + str(self.__id))
        self.__mother.do_signaling_device()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_checking_if_not_already_running(self) -> None:
        """!
        Will start the task which checks if the error is still busy
        @return: None
        """
        if self.__busy is False:
            thread = threading.Thread(target = self.task)
            thread.start()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

