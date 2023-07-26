from robohatlib.Robohat import Robohat
import time
from enum import Enum
from enum import IntEnum

# --------------------------------------------------------------------------------------
"""     +---------+
        |         |
[1]-----+         +-----[2]
        |         |
        +----+----+
             |
            [3]
             |
            [4]
             |
[5]----------+-=--------[6]

"""


ARRAY_POS_LEFT_FRONT_LEG_SERVO = 0
ARRAY_POS_RIGHT_FRONT_LEG_SERVO = 1
ARRAY_POS_NECK_SERVO = 2
ARRAY_POS_HIP_SERVO = 3
ARRAY_POS_LEFT_BACK_LEG_SERVO = 4
ARRAY_POS_RIGHT_BACK_LEG_SERVO = 5



TIME_BETWEEN_STEP = 5

LEG_NEUTRAL = 45.0
LEG_DOWN = 0
LEG_UP = 180.0


NECK_NEUTRAL = 90.0
NECK_LEFT = 0.0
NECK_RIGHT = 180.0

HIP_NEUTRAL = 90.0
HIP_LEFT = 0.0
HIP_RIGHT = 180.0


class ID(IntEnum):
    LEFT_FRONT_LEG = 1
    RIGHT_FRONT_LEG = 2
    NECK = 3
    HIP = 4
    LEFT_BACK_LEG = 5
    RIGHT_BACK_LEG = 6

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

        self.__servo_positions = [0.0] * 6

        self.set_servo_preset_value(ID.LEFT_FRONT_LEG, LEG_NEUTRAL)
        self.set_servo_preset_value(ID.RIGHT_FRONT_LEG, LEG_NEUTRAL)
        self.set_servo_preset_value(ID.NECK, NECK_NEUTRAL)
        self.set_servo_preset_value(ID.HIP, NECK_NEUTRAL)
        self.set_servo_preset_value(ID.LEFT_BACK_LEG, LEG_NEUTRAL)
        self.set_servo_preset_value(ID.RIGHT_BACK_LEG, LEG_NEUTRAL)

        self.push_preset_values_to_servos()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_walking(self) -> None:
        """
        The Robo hat will start walking
        @return: None
        """
        print("Started walking")

        running = True
        counter = 0

        while running:
            self._step_forward_right()
            self._step_forward_left()

            counter = counter + 1
            if counter > 10:
                running = False

        print("Stopped walking")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _step_forward_right(self):
        self._leg_right_front_up()
        self._joint_right()
        self._leg_right_front_neutral()
        self._joint_neutral()
        self._leg_left_back_up()
        self._joint_left()
        self._leg_left_back_neutral()
        self._joint_neutral()

        print("STALL")
        time.sleep(TIME_BETWEEN_STEP)
    # --------------------------------------------------------------------------------------

    def _step_forward_left(self):
        self._leg_left_front_up()
        self._joint_left()
        self._leg_left_front_neutral()
        self._joint_neutral()
        self._leg_right_back_up()
        self._joint_right()
        self._leg_right_back_neutral()
        self._joint_neutral()

        print("STALL")
        time.sleep(TIME_BETWEEN_STEP)
    # --------------------------------------------------------------------------------------

    # def _step_backward_right(self):
    #
    #     time.sleep(TIME_BETWEEN_STEP)
    # # --------------------------------------------------------------------------------------
    #
    # def _step_backward_left(self):
    #
    #     time.sleep(TIME_BETWEEN_STEP)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def push_preset_values_to_servos(self) -> None:
        unused_angle = 0.0

        angles = [unused_angle] * 32
        angles[ARRAY_POS_LEFT_FRONT_LEG_SERVO] =        self.get_servo_preset_value(ID.LEFT_FRONT_LEG)
        angles[ARRAY_POS_RIGHT_FRONT_LEG_SERVO] =       self.get_servo_preset_value(ID.RIGHT_FRONT_LEG)
        angles[ARRAY_POS_NECK_SERVO] =                  self.get_servo_preset_value(ID.NECK)
        angles[ARRAY_POS_HIP_SERVO] =                   self.get_servo_preset_value(ID.HIP)
        angles[ARRAY_POS_LEFT_BACK_LEG_SERVO] =         self.get_servo_preset_value(ID.LEFT_BACK_LEG)
        angles[ARRAY_POS_RIGHT_BACK_LEG_SERVO] =        self.get_servo_preset_value(ID.RIGHT_BACK_LEG)

        self.__robohat.set_servo_multiple_angles(angles)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_servo_preset_value(self, _servo_id:ID, _pos:float) -> None:
        servo_nr:int = int(_servo_id)

        self.__servo_positions[servo_nr-1] = _pos

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_servo_preset_value(self, _servo_id:ID) -> float:
        servo_nr: int = int(_servo_id)

        return self.__servo_positions[servo_nr-1]

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_right_front_up(self):
        print("_leg_right_front_up")
        self.set_servo_preset_value(ID.RIGHT_FRONT_LEG, LEG_UP)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_right_front_down(self):
        print("_leg_right_front_down")
        self.set_servo_preset_value(ID.RIGHT_FRONT_LEG, LEG_DOWN)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_right_front_neutral(self):
        print("_leg_right_front_neutral")
        self.set_servo_preset_value(ID.RIGHT_FRONT_LEG, LEG_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _leg_left_front_up(self):
        print("_leg_left_front_up")
        self.set_servo_preset_value(ID.LEFT_FRONT_LEG, LEG_UP)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_left_front_down(self):
        print("_leg_left_front_down")
        self.set_servo_preset_value(ID.LEFT_FRONT_LEG, LEG_DOWN)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_left_front_neutral(self):
        print("_leg_left_front_neutral")
        self.set_servo_preset_value(ID.LEFT_FRONT_LEG, LEG_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _leg_right_back_up(self):
        print("_leg_right_back_up")
        self.set_servo_preset_value(ID.RIGHT_BACK_LEG, LEG_UP)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_right_back_down(self):
        print("_leg_right_back_down")
        self.set_servo_preset_value(ID.RIGHT_BACK_LEG, LEG_DOWN)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_right_back_neutral(self):
        print("_leg_right_back_neutral")
        self.set_servo_preset_value(ID.RIGHT_BACK_LEG, LEG_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _leg_left_back_up(self):
        print("_leg_left_back_up")
        self.set_servo_preset_value(ID.LEFT_BACK_LEG, LEG_UP)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_left_back_down(self):
        print("_leg_left_back_down")
        self.set_servo_preset_value(ID.LEFT_BACK_LEG, LEG_DOWN)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_left_back_neutral(self):
        print("_leg_left_back_neutral")
        self.set_servo_preset_value(ID.LEFT_BACK_LEG, LEG_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _joint_right(self):
        print("_joint_right")
        self.set_servo_preset_value(ID.NECK, NECK_RIGHT)
        self.set_servo_preset_value(ID.HIP, HIP_LEFT)

        self.push_preset_values_to_servos()
        time.sleep(1)

    def _joint_left(self):
        print("_joint_left")
        self.set_servo_preset_value(ID.NECK, NECK_LEFT)
        self.set_servo_preset_value(ID.HIP, HIP_RIGHT)

        self.push_preset_values_to_servos()
        time.sleep(1)

    def _joint_neutral(self):
        print("_joint_neutral")
        self.set_servo_preset_value(ID.NECK, NECK_NEUTRAL)
        self.set_servo_preset_value(ID.HIP, NECK_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _neck_right(self):
        print("_neck_right")
        self.set_servo_preset_value(ID.NECK, NECK_RIGHT)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _neck_left(self):
        print("_neck_left")
        self.set_servo_preset_value(ID.NECK, NECK_LEFT)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _neck_neutral(self):
        print("_neck_neutral")
        self.set_servo_preset_value(ID.NECK, NECK_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _hip_right(self):
        print("_hip_right")
        self.set_servo_preset_value(ID.HIP, HIP_RIGHT)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _hip_left(self):
        print("_hip_left")
        self.set_servo_preset_value(ID.HIP, HIP_LEFT)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _hip_neutral(self):
        print("_hip_neutral")
        self.set_servo_preset_value(ID.HIP, HIP_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------