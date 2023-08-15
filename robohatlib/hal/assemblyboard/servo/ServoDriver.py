
try:
    import time
    import threading
    from enum import Enum
    from enum import IntEnum

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
        self.__direct_mode = True
        self.__delay_between_actions = 0.001
        self.__preset_servo_positions = [90.0] * 16
        self.__current_servo_positions = [90.0] * 16

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
        thread.daemon = True  # Daemonize thread
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

    def run(self):
        """!
        The actual timed update routne
        @return: None
        """

        while self.__running is True:
            if self.__direct_mode is False:
                for servo_nr in range(0, 16):
                    diff = self.__preset_servo_positions[servo_nr] - self.__current_servo_positions[servo_nr]
                    if diff < 0:
                        self.__current_servo_positions[servo_nr] = self.__current_servo_positions[servo_nr] - 1
                    elif diff > 0:
                        self.__current_servo_positions[servo_nr] = self.__current_servo_positions[servo_nr] + 1

                self.__servoboard.update_servo_data(self.__current_servo_positions)
                time.sleep(self.__delay_between_actions)                # wait (1 mS)
            else:                                                       # direct mode
                time.sleep(1)                                           # wait 1 S

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

        if self.__direct_mode is True:      # if direct_mode is false, timed update
            self.__current_servo_positions[_servo_index] = self.__preset_servo_positions[_servo_index]
            self.__servoboard.update_servo_data(self.__preset_servo_positions)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_servo_multiple_angles(self, _wanted_angles_array: []) -> None:
        """
        Set wanted servo angles (all)
        @param _wanted_angles_array:
        @return: None
        """
        for servo_index in range(0, len(_wanted_angles_array)):
            self.__preset_servo_positions[servo_index] = _wanted_angles_array[servo_index]

        if self.__direct_mode is True:       # if direct_mode is false, timed update
            for servo_index in range(0, len(_wanted_angles_array)):
                self.__current_servo_positions [servo_index] = self.__preset_servo_positions[servo_index]

            self.__servoboard.update_servo_data(self.__preset_servo_positions)


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