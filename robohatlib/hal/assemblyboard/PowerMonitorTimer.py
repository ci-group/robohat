"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

from __future__ import annotations

try:
    import time
    import threading
    from robohatlib.helpers.RoboUtil import RoboUtil
    from robohatlib.hal.assemblyboard import PowerMonitorAndIO
    from robohatlib.drivers.MCP23008 import MCP23008
    from robohatlib import RobohatConfig
    #import asyncio

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

    def __init__(self, _dc_dc_id:int, _mother:PowerMonitorAndIO, _expander:MCP23008, _name_of_assembly:str = ""):
        """!
        Constructor of this dataholder
        @param _dc_dc_id: id of this class
        """
        self.__dc_dc_id = _dc_dc_id
        self.__name_of_assembly = _name_of_assembly
        self.__mother = _mother
        self.__expander = _expander

        self.__task_loop_is_running = False

    #--------------------------------------------------------------------------------------

    def get_id(self) -> int:
        """!
        Returns ID of this dataholder
        @return:
        """
        return self.__dc_dc_id

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def task(self):
        """!
        Our running task which is a separate thread
        @return: None

        Will trigger the alarm when the I/O stays low in the time-window o has a multiple trigger pulses
        """

        start_time = RoboUtil.get_time_ms()
        last_error_time = RoboUtil.get_time_ms()

        while self.__task_loop_is_running:
            current_time = RoboUtil.get_time_ms()

            if self.__expander.get_pin_data(self.__dc_dc_id) == 0:        # still a short detected
                last_error_time = RoboUtil.get_time_ms()

                diff_time_current_start = current_time - start_time
                if diff_time_current_start >= RobohatConfig.TIME_WINDOW_OF_SHORT_PROTECTION_POWER_GOOD_CHECK_SERVO_POWER:
                    self.__trigger_error()
                    self.__task_loop_is_running = False
            else:
                diff_time_current_last_error = current_time - last_error_time
                if diff_time_current_last_error >= RobohatConfig.TIME_WINDOW_OF_SHORT_PROTECTION_RELEASE_SERVO_POWER:
                    self.__task_loop_is_running = False

            time.sleep(0.05)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_is_busy(self) -> bool:
        """!
        Return True when the task is Running
        @return: bool
        """
        return self.__task_loop_is_running

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __trigger_error(self) -> None:
        """!
        Will trigger an error message to the user
        @return: Nome
        """

        servo_id_min = self.__dc_dc_id * 4
        servo_id_max = servo_id_min + 3

        print("Major error: power fail DC/DC servo: " + str(servo_id_min) + " until " + str (servo_id_max) + " of: " + self.__name_of_assembly)
        self.__mother.do_signaling_device()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_checking_if_not_already_running(self) -> None:
        """!
        Will start the task which checks if the error is still busy
        @return: None
        """
        if self.__task_loop_is_running is False:
            self.__task_loop_is_running = True
            thread = threading.Thread(target = self.task)
            thread.start()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

