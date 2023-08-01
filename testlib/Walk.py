try:
    from robohatlib.Robohat import Robohat
    import time
    import threading
    import time
    from enum import Enum
    from enum import IntEnum

    from testlib.WalkDriver import WalkDriver
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
TIME_BETWEEN_STEP = 5

LEG_NEUTRAL = 45.0
LEG_DOWN = 10.0
LEG_UP = 90.0

NECK_NEUTRAL = 90.0
NECK_LEFT = 60.0
NECK_RIGHT = 120.0

HIP_NEUTRAL = 90.0
HIP_LEFT = 70.0
HIP_RIGHT = 110.0

DELAY_STEP = 1


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

        self.__walk_driver = WalkDriver(_robohat)

        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.HIP, NECK_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_NEUTRAL)

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

        self.__walk_driver.start_walking()

        counter = 0
        self.__running = True

        while self.__running:
            self._step_forward_right()
            self._step_forward_left()

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

        self.__walk_driver.stop_walking()
        self.__running = False
        print("Stopped walking")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _step_forward_right(self):
        self._leg_right_front_up()
        time.sleep(DELAY_STEP)

        self._joint_left()
        time.sleep(DELAY_STEP)

        self._leg_right_front_neutral()
        time.sleep(DELAY_STEP)

        self._joint_neutral()
        time.sleep(DELAY_STEP)

        self._leg_left_back_up()
        time.sleep(DELAY_STEP)

        self._joint_right()
        time.sleep(DELAY_STEP)

        self._leg_left_back_neutral()
        time.sleep(DELAY_STEP)

        self._joint_neutral()
        time.sleep(DELAY_STEP)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _step_forward_left(self):
        self._leg_left_front_up()
        time.sleep(DELAY_STEP)

        self._joint_right()
        time.sleep(DELAY_STEP)

        self._leg_left_front_neutral()
        time.sleep(DELAY_STEP)

        self._joint_neutral()
        time.sleep(DELAY_STEP)

        self._leg_right_back_up()
        time.sleep(DELAY_STEP)

        self._joint_left()
        time.sleep(DELAY_STEP)

        self._leg_right_back_neutral()
        time.sleep(DELAY_STEP)

        self._joint_neutral()
        time.sleep(DELAY_STEP)


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __set_servo_preset_value(self, _servo_id:WalkServoID, _pos:float) -> None:
        self.__walk_driver.set_servo_preset_value(_servo_id, _pos)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __get_servo_is_wanted_angle(self, _servo_id:WalkServoID) -> bool:
        return self.__walk_driver.get_servo_is_wanted_angle(_servo_id)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_right_front_up(self):
        print("_leg_right_front_up")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False:
            time.sleep(0.1)

    def _leg_right_front_down(self):
        print("_leg_right_front_down")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False:
            time.sleep(0.1)

    def _leg_right_front_neutral(self):
        print("_leg_right_front_neutral")
        self.__set_servo_preset_value(WalkServoID.RIGHT_FRONT_LEG, LEG_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_FRONT_LEG) is False:
            print("_leg_right_front_neutral zzz")
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_left_front_up(self):
        print("_leg_left_front_up")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False:
            time.sleep(0.1)


    def _leg_left_front_down(self):
        print("_leg_left_front_down")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False:
            time.sleep(0.1)

    def _leg_left_front_neutral(self):
        print("_leg_left_front_neutral")
        self.__set_servo_preset_value(WalkServoID.LEFT_FRONT_LEG, LEG_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_FRONT_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_right_back_up(self):
        print("_leg_right_back_up")
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    def _leg_right_back_down(self):
        print("_leg_right_back_down")
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    def _leg_right_back_neutral(self):
        print("_leg_right_back_neutral")
        self.__set_servo_preset_value(WalkServoID.RIGHT_BACK_LEG, LEG_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.RIGHT_BACK_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_left_back_up(self):
        print("_leg_left_back_up")
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_UP)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    def _leg_left_back_down(self):
        print("_leg_left_back_down")
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_DOWN)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    def _leg_left_back_neutral(self):
        print("_leg_left_back_neutral")
        self.__set_servo_preset_value(WalkServoID.LEFT_BACK_LEG, LEG_NEUTRAL)
        while self.__get_servo_is_wanted_angle(WalkServoID.LEFT_BACK_LEG) is False:
            time.sleep(0.1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _joint_right(self):
        print("_joint_right")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_RIGHT)
        self.__set_servo_preset_value(WalkServoID.HIP, HIP_LEFT)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    def _joint_left(self):
        print("_joint_left")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_LEFT)
        self.__set_servo_preset_value(WalkServoID.HIP, HIP_RIGHT)
        while self.__get_servo_is_wanted_angle(WalkServoID.NECK) is False or self.__get_servo_is_wanted_angle(WalkServoID.HIP) is False:
            time.sleep(0.1)

    def _joint_neutral(self):
        print("_joint_neutral")
        self.__set_servo_preset_value(WalkServoID.NECK, NECK_NEUTRAL)
        self.__set_servo_preset_value(WalkServoID.HIP, NECK_NEUTRAL)
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
