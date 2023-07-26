from robohatlib.Robohat import Robohat
import time

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

LEFT_FRONT_LEG_SERVO = 1
RIGHT_FRONT_LEG_SERVO = 2
NECK_SERVO = 3
HIP_SERVO = 4
LEFT_BACK_LEG_SERVO = 5
RIGHT_BACK_LEG_SERVO = 6

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

        self.set_servo_preset_value(LEFT_FRONT_LEG_SERVO, LEG_NEUTRAL)
        self.set_servo_preset_value(RIGHT_FRONT_LEG_SERVO, LEG_NEUTRAL)
        self.set_servo_preset_value(NECK_SERVO, NECK_NEUTRAL)
        self.set_servo_preset_value(HIP_SERVO, NECK_NEUTRAL)
        self.set_servo_preset_value(LEFT_BACK_LEG_SERVO, LEG_NEUTRAL)
        self.set_servo_preset_value(RIGHT_BACK_LEG_SERVO, LEG_NEUTRAL)

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
        unused_angle = 0

        self.__robohat.set_servo_multiple_angles(
                                                [self.get_servo_preset_value(1),
                                                 self.get_servo_preset_value(2),
                                                 self.get_servo_preset_value(3),
                                                 self.get_servo_preset_value(4),
                                                 self.get_servo_preset_value(5),
                                                 self.get_servo_preset_value(6),
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle,
                                                 unused_angle])

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_servo_preset_value(self, _servo_nr:int, _pos:float) -> None:
        if _servo_nr < 1 or _servo_nr > 6:
            return

        self.__servo_positions[_servo_nr-1] = _pos

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_servo_preset_value(self, _servo_nr:int) -> float:
        if _servo_nr < 1 or _servo_nr > 6:
            return -1

        return self.__servo_positions[_servo_nr-1]

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def _leg_right_front_up(self):
        self.set_servo_preset_value(RIGHT_FRONT_LEG_SERVO, LEG_UP)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_right_front_down(self):
        self.set_servo_preset_value(RIGHT_FRONT_LEG_SERVO, LEG_DOWN)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_right_front_neutral(self):
        self.set_servo_preset_value(RIGHT_FRONT_LEG_SERVO, LEG_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _leg_left_front_up(self):
        self.set_servo_preset_value(LEFT_FRONT_LEG_SERVO, LEG_UP)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_left_front_down(self):
        self.set_servo_preset_value(LEFT_FRONT_LEG_SERVO, LEG_DOWN)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_left_front_neutral(self):
        self.set_servo_preset_value(LEFT_FRONT_LEG_SERVO, LEG_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _leg_right_back_up(self):
        self.set_servo_preset_value(RIGHT_BACK_LEG_SERVO, LEG_UP)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_right_back_down(self):
        self.set_servo_preset_value(RIGHT_BACK_LEG_SERVO, LEG_DOWN)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_right_back_neutral(self):
        self.set_servo_preset_value(RIGHT_BACK_LEG_SERVO, LEG_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _leg_left_back_up(self):
        self.set_servo_preset_value(LEFT_BACK_LEG_SERVO, LEG_UP)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_left_back_down(self):
        self.set_servo_preset_value(LEFT_BACK_LEG_SERVO, LEG_DOWN)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _leg_left_back_neutral(self):
        self.set_servo_preset_value(LEFT_BACK_LEG_SERVO, LEG_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _joint_right(self):
        self.set_servo_preset_value(NECK_SERVO, NECK_RIGHT)
        self.set_servo_preset_value(HIP_SERVO, HIP_LEFT)

        self.push_preset_values_to_servos()
        time.sleep(1)

    def _joint_left(self):
        self.set_servo_preset_value(NECK_SERVO, NECK_LEFT)
        self.set_servo_preset_value(HIP_SERVO, HIP_RIGHT)

        self.push_preset_values_to_servos()
        time.sleep(1)

    def _joint_neutral(self):
        self.set_servo_preset_value(NECK_SERVO, NECK_NEUTRAL)
        self.set_servo_preset_value(HIP_SERVO, NECK_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _neck_right(self):
        self.set_servo_preset_value(NECK_SERVO, NECK_RIGHT)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _neck_left(self):
        self.set_servo_preset_value(NECK_SERVO, NECK_LEFT)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _neck_neutral(self):
        self.set_servo_preset_value(NECK_SERVO, NECK_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------

    def _hip_right(self):
        self.set_servo_preset_value(HIP_SERVO, HIP_RIGHT)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _hip_left(self):
        self.set_servo_preset_value(HIP_SERVO, HIP_LEFT)
        self.push_preset_values_to_servos()
        time.sleep(1)

    def _hip_neutral(self):
        self.set_servo_preset_value(HIP_SERVO, HIP_NEUTRAL)
        self.push_preset_values_to_servos()
        time.sleep(1)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------