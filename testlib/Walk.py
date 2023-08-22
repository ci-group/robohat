try:
    from robohatlib.Robohat import Robohat
    import time
    import threading
    import time
    from enum import Enum
    from enum import IntEnum

    from testlib.WalkServoID import WalkServoID

except ImportError:
    print("Failed to import needed dependencies for the Walk class")
    raise


# --------------------------------------------------------------------------------------
"""     +---------+
        |         |
[0]-----+         +-----[1]
        |         |
        +----+----+
             |
            [2]
             |
            [3]
             |
[4]----------+-=--------[5]

"""

# CONSTANTS BELOW ARE THE SERVO NR OF THE HARDWARE SERVO. mAY NOT EXCEED 32
LEFT_FRONT_LEG_SERVO_NR = 0
RIGHT_FRONT_LEG_SERVO_NR = 1
NECK_SERVO_NR = 2
HIP_SERVO_NR = 3
LEFT_BACK_LEG_SERVO_NR = 4
RIGHT_BACK_LEG_SERVO_NR = 5

# OTHER CONSTANTS
TIME_BETWEEN_STEP = 0.1

LEG_FRONT_NEUTRAL = 90.0
LEG_FRONT_DOWN = 30.0
LEG_FRONT_UP = 125.0

LEG_BACK_NEUTRAL = 90.0
LEG_BACK_DOWN = 20.0
LEG_BACK_UP = 150.0

NECK_NEUTRAL = 90.0
NECK_LEFT = 60.0
NECK_RIGHT = 120.0

HIP_NEUTRAL = 90.0
HIP_LEFT = 60.0
HIP_RIGHT = 120.0

DELAY_STEP = 0.1

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

class Walk:

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


    def __init__(self, _robohat:Robohat):
        """!
        Constructor
        @param _robohat: The Robohat lib class
        """
        self.__robohat = _robohat

        self.__robohat.set_servo_direct_mode(False)

        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_FRONT_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_FRONT_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.HIP, NECK_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_BACK_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_BACK_NEUTRAL)

        self.__running = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_walking(self) -> None:
        """!
        The Robohat will start walking
        @return: None
        """

        print("Started walking")
        print ("1")
        self._side_right_neutral()
        self._side_left_neutral()
        self._joint_neutral()
        time.sleep(5)

        counter = 0
        self.__running = True

        while self.__running:

            self._step_forward()
            time.sleep(TIME_BETWEEN_STEP)

            # self._step_forward_left()
            # time.sleep(TIME_BETWEEN_STEP)

            counter = counter + 1
            if counter > 10:
                self.__running = False

        self.stop_walking()


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def stop_walking(self) -> None:
        """!
        The Robohat will stop with walking
        @return: None
        """

        self.__running = False
        print("Stopped walking")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _step_forward(self):

        # we are standing in a neutral pos
        print ("2")
        self._joint_left()
        time.sleep(DELAY_STEP)

        print ("3")
        self._side_right_down()
        time.sleep(DELAY_STEP)

        print ("3")
        self._joint_neutral()
        time.sleep(DELAY_STEP)

        print ("4")
        self._side_right_neutral()
        time.sleep(DELAY_STEP)

        # #--------------------------------
        print ("5")
        self._joint_right()
        time.sleep(DELAY_STEP)

        print ("6")
        self._side_left_down()
        time.sleep(DELAY_STEP)

        print ("7")
        self._joint_neutral()
        time.sleep(DELAY_STEP)

        print ("8")
        self._side_left_neutral()
        time.sleep(DELAY_STEP)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __set_servo_preset_value(self, _servo_id:WalkServoID, _pos:float) -> None:
        servo_nr: int = int(_servo_id)
        self.__robohat.set_servo_single_angle(servo_nr, _pos)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __get_servo_is_wanted_angle(self, _servo_id:WalkServoID) -> bool:
        servo_nr: int = int(_servo_id)
        return self.__robohat.get_servo_is_single_servo_wanted_angle(servo_nr)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_right_front_up(self):
        print("_leg_right_front_up")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_FRONT_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False:
            time.sleep(0.1)

    def _leg_right_front_down(self):
        print("_leg_right_front_down")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_FRONT_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False:
            time.sleep(0.1)

    def _leg_right_front_neutral(self):
        print("_leg_right_front_neutral")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_FRONT_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_left_front_up(self):
        print("_leg_left_front_up")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_FRONT_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False:
            time.sleep(0.1)


    def _leg_left_front_down(self):
        print("_leg_left_front_down")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_FRONT_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False:
            time.sleep(0.1)

    def _leg_left_front_neutral(self):
        print("_leg_left_front_neutral")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_FRONT_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_right_back_up(self):
        print("_leg_right_back_up")
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_BACK_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    def _leg_right_back_down(self):
        print("_leg_right_back_down")
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_BACK_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    def _leg_right_back_neutral(self):
        print("_leg_right_back_neutral")
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_BACK_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_left_back_up(self):
        print("_leg_left_back_up")
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_BACK_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    def _leg_left_back_down(self):
        print("_leg_left_back_down")
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_BACK_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    def _leg_left_back_neutral(self):
        print("_leg_left_back_neutral")
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_BACK_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _side_right_up(self):
        print("_side_right_up")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_FRONT_UP)
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_BACK_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False or self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    def _side_right_down(self):
        print("_side_right_down")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_FRONT_DOWN)
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_BACK_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False or self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    def _side_right_neutral(self):
        print("_side_right_neutral")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_FRONT_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_BACK_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False or self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _side_left_up(self):
        print("_leg_right_front_up")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_FRONT_UP)
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_BACK_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False or self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    def _side_left_down(self):
        print("_leg_right_front_down")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_FRONT_DOWN)
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_BACK_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False or self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    def _side_left_neutral(self):
        print("_leg_right_front_neutral")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_FRONT_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_BACK_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False or self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _joint_right(self):
        print("_joint_right")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_RIGHT)
        self.__set_servo_preset_value(WalkServoID.HIP, HIP_RIGHT)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    def _joint_left(self):
        print("_joint_left")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_LEFT)
        self.__set_servo_preset_value(WalkServoID.HIP, HIP_LEFT)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    def _joint_neutral(self):
        print("_joint_neutral")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.HIP, HIP_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _neck_right(self):
        print("_neck_right")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_RIGHT)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    def _neck_left(self):
        print("_neck_left")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_LEFT)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    def _neck_neutral(self):
        print("_neck_neutral")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _hip_right(self):
        print("_hip_right")
        self.__set_servo_preset_value(WalkServoID.HIP, HIP_RIGHT)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    def _hip_left(self):
        print("_hip_left")
        self.__set_servo_preset_value(WalkServoID.HIP, HIP_LEFT)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    def _hip_neutral(self):
        print("_hip_neutral")
        self.__set_servo_preset_value(WalkServoID.HIP, HIP_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
