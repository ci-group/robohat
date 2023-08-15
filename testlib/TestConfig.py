#!/usr/bin/env python

try:
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib import RobohatConstants
    from robohatlib.PwmPlug import PwmPlug
except ImportError:
    print("Failed to import all dependencies for TestConfig")
    raise


#INITIAL_VOLT_TO_ANGLE_FORMULA_A = 73.00                             # part A of the formula servo voltage to angle (y = Ax + B)
#INITIAL_VOLT_TO_ANGLE_FORMULA_B = -12.45                            # part B of the formula servo voltage to angle (y = Ax + B)

INITIAL_VOLT_TO_ANGLE_FORMULA_A =  68.50117096018737
INITIAL_VOLT_TO_ANGLE_FORMULA_B =  -15.294412847106067

SERVOASSEMBLY_1_NAME = "servoassembly_1"                    # just a name for own reference
SERVOASSEMBLY_1_SW1_PWM_ADDRESS = 0                         # sw1 value of the servo assembly
SERVOASSEMBLY_1_SW2_POWER_GOOD_ADDRESS = 0                  # sw2 value of the servo assembly
SERVOASSEMBLY_1_PWM_PLUG = PwmPlug.PWMPLUG_P3     # connected port of the tophat board, is actual the cs of the SPI bus

SERVOBOARD_1_DATAS_ARRAY = [
                    ServoData( 0, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 1, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 2, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 3, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 4, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 5, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 6, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 7, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 8, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 9, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(10, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(11, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(12, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(13, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(14, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(15, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ]                                       # array with servo settings : servo nr, min time us, max time us, max range degree, degree offset, formula A, formula B

servoassembly_1_config = ServoAssemblyConfig(SERVOASSEMBLY_1_NAME,
                                             SERVOASSEMBLY_1_SW1_PWM_ADDRESS,
                                             SERVOASSEMBLY_1_SW2_POWER_GOOD_ADDRESS,
                                             SERVOASSEMBLY_1_PWM_PLUG)

#--------------------

SERVOASSEMBLY_2_NAME = "servoassembly_2"                    # just a name for own reference
SERVOASSEMBLY_2_SW1_PWM_ADDRESS = 1                         # sw1 value of the servo assembly
SERVOASSEMBLY_2_SW2_POWER_GOOD_ADDRESS = 1                  # sw2 value of the servo assembly
SERVOASSEMBLY_2_PWMPLUG = PwmPlug.PWMPLUG_P4      # connected port of the tophat board, is actual the cs of the SPI bus



SERVOBOARD_2_DATAS_ARRAY = [
                    ServoData( 0, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 1, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 2, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 3, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 4, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 5, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 6, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 7, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 8, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData( 9, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(10, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(11, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(12, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(13, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(14, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ServoData(15, 500, 2500, 180, 0, INITIAL_VOLT_TO_ANGLE_FORMULA_A, INITIAL_VOLT_TO_ANGLE_FORMULA_B),
                    ]                       # array with servo settings :           servo nr, min time us, max time us, max range degree, degree offset, formula A, formula B

servoassembly_2_config = ServoAssemblyConfig(SERVOASSEMBLY_2_NAME,
                                             SERVOASSEMBLY_2_SW1_PWM_ADDRESS,
                                             SERVOASSEMBLY_2_SW2_POWER_GOOD_ADDRESS,
                                             SERVOASSEMBLY_2_PWMPLUG)

#--------------------

TOPBOARD_IO_EXPANDER_SW = 7         # switch value of the dip switch onto the topboard. Default value is 7

#--------------------
