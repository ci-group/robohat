
try:
    from robohatlib.Robohat import Robohat
    import time
    import threading
    import time
    from enum import Enum
    from enum import IntEnum
    from testlib.WalkServoID import WalkServoID

except ImportError:
    print("Failed to import needed dependencies for the WalkDriver class")
    raise

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

class WalkDriver:

    def __init__(self, _robohat:Robohat):
        """!
         Constructor
        """
        print("Constructor of WalkDriver")
        self.__robohat = _robohat

        self.__running = False
        self.__preset_servo_positions = [90.0] * 32
        self.__current_servo_positions = [90.0] * 32

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_walking(self) -> None:
        print("start_walking")

        self.__running = True
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def stop_walking(self) -> None:
        print("stop_walking")

        self.__running = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def run(self):
        while self.__running is True:
            length:int = len(self.__preset_servo_positions)

            for servo_nr in range( length ):
                diff = self.__preset_servo_positions[servo_nr] - self.__current_servo_positions[servo_nr]
                if diff < 0:
                    self.__current_servo_positions[servo_nr] = self.__current_servo_positions[servo_nr] - 1
                elif diff > 0:
                    self.__current_servo_positions[servo_nr] = self.__current_servo_positions[servo_nr] + 1

            self.__robohat.set_servo_multiple_angles(self.__current_servo_positions)

            time.sleep(0.001)  # wait 1 mS

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_servo_is_wanted_angle(self, _servo_id:WalkServoID) -> bool:
        servo_nr: int = int(_servo_id)
        angle_preset = self.__preset_servo_positions[servo_nr]

        angle_low = angle_preset
        angle_high = angle_preset + 1

        #print(str(angle_low ) + " < " + str(angle_preset) + " < " + str(angle_high) )
        if angle_preset >= angle_low and angle_preset <= angle_high:
            return True
        else:
            return False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_servo_preset_value(self, _servo_id: WalkServoID, _pos: float) -> None:
        array_pos_servo_pos: int = int(_servo_id)
        self.__preset_servo_positions[array_pos_servo_pos] = _pos

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __get_servo_preset_value(self, _servo_id:WalkServoID) -> float:
        array_pos_servo_pos:int = int(_servo_id)

        return self.__preset_servo_positions[array_pos_servo_pos]

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------