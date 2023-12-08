"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    import threading
    from enum import Enum
    from enum import IntEnum
    # import asyncio
    from robohatlib import RobohatConfig
    import time

except ImportError:
    print("Failed to import needed dependencies for the ServoDriver class")
    raise

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

class ServoDriver:
    """!
    Will update the angles of the servo direct, ir periodically
    """

    def __init__(self, _servoboard):
        """!
         Constructor
        """
        print("Constructor of ServoDriver")
        self.__servoboard = _servoboard

        self.__running = False
        self.__i_am_a_sleep = False
        self.__direct_mode = True
        self.__delay_between_actions = RobohatConfig.DEFAULT_DELAY_BETWEEN_ACTION
        self.__preset_servo_positions = [RobohatConfig.INITIAL_POS_OF_SERVOS] * 16
        self.__current_servo_positions = [RobohatConfig.INITIAL_POS_OF_SERVOS] * 16
        self.__update_value = RobohatConfig.DEFAULT_SERVO_UPDATE_VALUE

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_driver(self, _current_servo_positions = None) -> None:
        """!
        Starts this driver
        @param _current_servo_positions:
        @return: None
        """
        # set default value. if none, default is already 90 degree, see constructor
        if _current_servo_positions is not None:
            for i in range(0, len(_current_servo_positions)):
                self.__current_servo_positions[i] = _current_servo_positions[i]

        self.__running = True
        thread = threading.Thread(target=self.run, args=())
        thread.start()  # Start the execution

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def stop_driver(self) -> None:
        """!
        Stops this driver
        @return: None
        """
        self.__running = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_direct_mode(self, _mode:bool) -> None:
        """!
        Set drive mode
        @param _mode: the mode, true is direct drive mode
        @return: None
        """

        self.__direct_mode = _mode

        # be sure that the settings are in sync
        if self.__direct_mode is True:       # if direct_mode is false, timed update
            for servo_index in range(0, len(self.__preset_servo_positions)):
                self.__current_servo_positions [servo_index] = self.__preset_servo_positions[servo_index]

            self.__servoboard.update_servo_data(self.__preset_servo_positions)

    # --------------------------------------------------------------------------------------

    def get_is_direct_mode(self) -> bool:
        """!
        Returns True if the driver is in direct mode
        @return: bool
        """

        return self.__direct_mode

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_delay(self, _delay:float) -> None:
        """!
        @param _delay:
        @return: None
        """

        self.__delay_between_actions = _delay

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_update_value(self, _update_value: int) -> None:
        """!
        Set value which is used to add or subtract from current pos
        """
        self.__update_value = _update_value

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def run(self):
        """!
        The actual timed update routine
        When sleeping just a periodic loop

        When in Time mode (not direct) will update __current_servo_positions with self.__update_value (ot 1) until __preset_servo_positions[servo_nr]
        In Direct mode __current_servo_positions = __preset_servo_positions[servo_nr]

        @return: None
        """

        while self.__running is True:
            if self.__i_am_a_sleep is True:
                time.sleep(0.1)                                # wait (100 mS)
            elif self.__direct_mode is False:
                for servo_nr in range(0, 16):
                    diff = self.__preset_servo_positions[servo_nr] - self.__current_servo_positions[servo_nr]
                    if abs(diff) > self.__update_value:
                        if diff < 0:
                            self.__current_servo_positions[servo_nr] = self.__current_servo_positions[servo_nr] - self.__update_value
                        elif diff > 0:
                            self.__current_servo_positions[servo_nr] = self.__current_servo_positions[servo_nr] + self.__update_value
                    else:   # old way to prevent over or undershoot
                        if diff < 0:
                            self.__current_servo_positions[servo_nr] = self.__current_servo_positions[servo_nr] - 1
                        elif diff > 0:
                            self.__current_servo_positions[servo_nr] = self.__current_servo_positions[servo_nr] + 1

                self.__servoboard.update_servo_data(self.__current_servo_positions)
                time.sleep(self.__delay_between_actions)       # wait
            else:                                                       # direct mode
                # update current array with wanted values
                for servo_nr in range(0, 16):
                    self.__current_servo_positions[servo_nr] = self.__preset_servo_positions[servo_nr]

                self.__servoboard.update_servo_data(self.__current_servo_positions)
                time.sleep(self.__delay_between_actions)       # wait

    #--------------------------------------------------------------------------------------

    def put_to_sleep(self) -> None:
        """!
        Put the device into a sleep state
        @return: None
        """
        self.__i_am_a_sleep = True

    #--------------------------------------------------------------------------------------

    def wake_up(self) -> None:
        """!
        Wakes up device
        @return: None
        """
        self.__i_am_a_sleep = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_servo_single_angle(self, _servo_index: int, _wanted_angle: float) -> None:
        """
        Set wanted servo angle (single servo)
        @param _servo_index: the servo
        @param _wanted_angle the angle
        @return: None
        """

        self.__preset_servo_positions[_servo_index] = _wanted_angle

        #update done in run loop
        #if self.__direct_mode is True:      # if direct_mode is false, timed update
        #    self.__current_servo_positions[_servo_index] = self.__preset_servo_positions[_servo_index]
        #    self.__servoboard.update_servo_data(self.__preset_servo_positions)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_servo_multiple_angles(self, _wanted_angles_list: []) -> None:
        """
        Set wanted servo angles (all)
        @param _wanted_angles_list:
        @return: None
        """
        for servo_index in range(0, len(_wanted_angles_list)):
            self.__preset_servo_positions[servo_index] = _wanted_angles_list[servo_index]

        if self.__direct_mode is True:       # if direct_mode is false, timed update
            for servo_index in range(0, len(_wanted_angles_list)):
                self.__current_servo_positions [servo_index] = self.__preset_servo_positions[servo_index]
            ##self.__servoboard.update_servo_data(self.__preset_servo_positions)                        # should be updated by thread

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_servo_is_single_servo_wanted_angle(self, _servo_index:int) -> bool:
        """!
        Returns true if (previous) wanted angle the same as the angle of the servo

        @param _servo_index: The sero index
        @return: bool
        """

        angle_preset = self.__preset_servo_positions[_servo_index]

        angle_low = self.__current_servo_positions[_servo_index] - 1
        angle_high = self.__current_servo_positions[_servo_index] + 1

        #print(str(angle_low ) + " < " + str(angle_preset) + " < " + str(angle_high) )

        if angle_preset >= angle_low and angle_preset <= angle_high:
            return True
        else:
            return False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------