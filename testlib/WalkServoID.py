"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

A enum to which is used in the Walk test routine

"""

try:
    from enum import Enum
    from enum import IntEnum
except ImportError:
    print("Failed to import needed dependencies for the WalkServoID class")
    raise


class WalkServoID(IntEnum):
    """!
    Internal ID. Maps to an array. ID nr should be lower than the size of the array ( < 32 )
    """
    LEFT_FRONT_LEG = 0
    RIGHT_FRONT_LEG = 1
    NECK = 2
    HIP = 3
    LEFT_BACK_LEG = 4
    RIGHT_BACK_LEG = 5