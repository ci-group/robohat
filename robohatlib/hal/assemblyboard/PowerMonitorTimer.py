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
    This class will monitor the pin which caused the interrupt if a short still occurs
    """

    def __init__(self, _id:int, _mother:PowerMonitorAndIO, _expander:MCP23008):
        """!
        Constructor of this dataholder
        @param _id: id of this class
        """
        self.__id = _id
        self.__mother = _mother
        self.__expander = _expander

        print("yeay " + str(_id))
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
        blocking = True
        start_time = RoboUtil.get_time_ms()
        last_check = RoboUtil.get_time_ms()

        while blocking:
            current_time = RoboUtil.get_time_ms()
            diff_time = current_time - start_time

            if self.__expander.get_pin_data(self.__id) == 1:        # pin when high, so no short anymore. is in the threshold. so no alarm, get out of this loop
                blocking = False
            else:
                if diff_time >= RobohatConfig.TIME_WINDOW_TO_BE_DCDC_SHORT_TO_ALARM:
                    blocking = False
                    self._display_error()

            time.sleep(0.1)

        self.__mother.remove_from_list(self.__id)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _display_error(self):
        print("Major error: power fail DC/DC " + str(self.__id))
        self.__mother.do_signaling_device()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def check(self) -> None:
        thread = threading.Thread(target = self.task)
        thread.start()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

