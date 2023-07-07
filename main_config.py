#!/usr/bin/env python

from robohatlib.Robohat import Robohat
from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
from robohatlib import Robohat_constants

SERVOASSEMBLY_1_NAME = "ServoAssembly_0"                    # just a name for own reference
SERVOASSEMBLY_1_SW1_PWM_ADDRESS = 0                         # sw1 value of the servo assembly
SERVOASSEMBLY_1_SW2_POWER_GOOD_ADDRESS = 0                  # sw2 value of the servo assembly
SERVOASSEMBLY_1_PWMPLUG = Robohat_constants.PWMPLUG_P3      # connected port of the topboard
SERVOBOARD_1_DATAS_ARRAY = [
                    ServoData(1, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(2, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(3, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(4, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(5, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(6, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(7, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(8, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(9, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(10, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(11, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(12, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(13, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(14, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(15, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(16, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ]

servoassembly_1_config = ServoAssemblyConfig(SERVOASSEMBLY_1_NAME,
                                             SERVOASSEMBLY_1_SW1_PWM_ADDRESS,
                                             SERVOASSEMBLY_1_SW2_POWER_GOOD_ADDRESS,
                                             SERVOASSEMBLY_1_PWMPLUG)

#--------------------

SERVOASSEMBLY_2_NAME = "ServoAssembly_1"                    # just a name for own reference
SERVOASSEMBLY_2_SW1_PWM_ADDRESS = 1                         # sw1 value of the servo assembly
SERVOASSEMBLY_2_SW2_POWER_GOOD_ADDRESS = 1                  # sw2 value of the servo assembly
SERVOASSEMBLY_2_PWMPLUG = Robohat_constants.PWMPLUG_P4      # connected port of the topboard
SERVOBOARD_2_DATAS_ARRAY = [
                    ServoData(1, 500, 2500, 180, 0, 72.2058435743876, -22.0429203374794),
                    ServoData(2, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(3, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(4, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(5, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(6, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(7, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(8, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(9, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(10, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(11, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(12, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(13, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(14, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(15, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ServoData(16, 500, 2500, 180, 0, 72.2058435743876, -22.8429203374794),
                    ]

servoassembly_2_config = ServoAssemblyConfig(SERVOASSEMBLY_2_NAME,
                                             SERVOASSEMBLY_2_SW1_PWM_ADDRESS,
                                             SERVOASSEMBLY_2_SW2_POWER_GOOD_ADDRESS,
                                             SERVOASSEMBLY_2_PWMPLUG)

#--------------------

TOPBOARD_IOEXANDER_SW = 7

#--------------------
