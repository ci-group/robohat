from robohatlib.Robohat import Robohat
import time
from enum import Enum
from enum import IntEnum

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
LEG_DOWN = 10
LEG_UP = 90.0

NECK_NEUTRAL = 90.0
NECK_LEFT = 80.0
NECK_RIGHT = 100.0

HIP_NEUTRAL = 80.0
HIP_LEFT = 30.0
HIP_RIGHT = 150.0




class ID(IntEnum):
    """
    Internal ID. Maps to an array. ID nr should be lower than the size of the array ( < 32 )
    """
    LEFT_FRONT_LEG = 0
    RIGHT_FRONT_LEG = 1
    NECK = 2
    HIP = 3
    LEFT_BACK_LEG = 4
    RIGHT_BACK_LEG = 5

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

        self.__servo_positions = [0.0] * 32

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
        angles[LEFT_FRONT_LEG_SERVO_NR] =        self.get_servo_preset_value(ID.LEFT_FRONT_LEG)
        angles[RIGHT_FRONT_LEG_SERVO_NR] =       self.get_servo_preset_value(ID.RIGHT_FRONT_LEG)
        angles[NECK_SERVO_NR] =                  self.get_servo_preset_value(ID.NECK)
        angles[HIP_SERVO_NR] =                   self.get_servo_preset_value(ID.HIP)
        angles[LEFT_BACK_LEG_SERVO_NR] =         self.get_servo_preset_value(ID.LEFT_BACK_LEG)
        angles[RIGHT_BACK_LEG_SERVO_NR] =        self.get_servo_preset_value(ID.RIGHT_BACK_LEG)

        self.__robohat.set_servo_multiple_angles(angles)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_servo_preset_value(self, _servo_id:ID, _pos:float) -> None:
        array_pos_servo_pos:int = int(_servo_id)

        self.__servo_positions[array_pos_servo_pos] = _pos

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_servo_preset_value(self, _servo_id:ID) -> float:
        array_pos_servo_pos:int = int(_servo_id)

        return self.__servo_positions[array_pos_servo_pos]

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