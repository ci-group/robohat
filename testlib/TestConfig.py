"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Just an configuration as needed, and used in the test routines
"""

try:
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib import RobohatConstants
    from robohatlib.hal.assemblyboard.PwmPlug import PwmPlug
except ImportError:
    print("Failed to import all dependencies for TestConfig")
    raise

INITIAL_VOLT_TO_ANGLE_FORMULA_A = (
    68.50117096018737  # parameter A of the formula servo voltage to angle (y = Ax + B)
)
INITIAL_VOLT_TO_ANGLE_FORMULA_B = (
    -15.294412847106067
)  # parameter B of the formula servo voltage to angle (y = Ax + B)

SERVOASSEMBLY_1_NAME = "servoassembly_1"  # just a name for own reference
SERVOASSEMBLY_1_SW1_PWM_ADDRESS = 0  # sw1 value of the servo assembly
SERVOASSEMBLY_1_SW2_POWER_GOOD_ADDRESS = 0  # sw2 value of the servo assembly
SERVOASSEMBLY_1_PWM_PLUG = (
    PwmPlug.PWMPLUG_P3
)  # connected port of the tophat board, is actual the cs of the SPI bus

SERVOBOARD_1_DATAS_LIST = [
    ServoData(
        0,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        1,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        2,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        3,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        4,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        5,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        6,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        7,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        8,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        9,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        10,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        11,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        12,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        13,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        14,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        15,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
]
# list with servo settings : servo nr, min time us, max time us, offset time us, max range degree, degree offset, formula A, formula B

SERVOASSEMBLY_1_CONFIG = ServoAssemblyConfig(
    SERVOASSEMBLY_1_NAME,
    SERVOASSEMBLY_1_SW1_PWM_ADDRESS,
    SERVOASSEMBLY_1_SW2_POWER_GOOD_ADDRESS,
    SERVOASSEMBLY_1_PWM_PLUG,
)

# --------------------

SERVOASSEMBLY_2_NAME = "servoassembly_2"  # just a name for own reference
SERVOASSEMBLY_2_SW1_PWM_ADDRESS = 1  # sw1 value of the servo assembly
SERVOASSEMBLY_2_SW2_POWER_GOOD_ADDRESS = 1  # sw2 value of the servo assembly
SERVOASSEMBLY_2_PWMPLUG = (
    PwmPlug.PWMPLUG_P4
)  # connected port of the tophat board, is actual the cs of the SPI bus

SERVOBOARD_2_DATAS_LIST = [
    ServoData(
        0,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        1,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        2,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        3,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        4,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        5,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        6,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        7,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        8,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        9,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        10,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        11,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        12,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        13,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        14,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
    ServoData(
        15,
        500,
        2500,
        0,
        180,
        0,
        INITIAL_VOLT_TO_ANGLE_FORMULA_A,
        INITIAL_VOLT_TO_ANGLE_FORMULA_B,
    ),
]
# list with servo settings :           servo nr, min time us, max time us, offset time us, max range degree, degree offset, formula A, formula B

SERVOASSEMBLY_2_CONFIG = ServoAssemblyConfig(
    SERVOASSEMBLY_2_NAME,
    SERVOASSEMBLY_2_SW1_PWM_ADDRESS,
    SERVOASSEMBLY_2_SW2_POWER_GOOD_ADDRESS,
    SERVOASSEMBLY_2_PWMPLUG,
)

# --------------------

TOPBOARD_ID_SWITCH = (
    7  # switch value of the dip switch onto the topboard. Default value is 7
)

# --------------------
