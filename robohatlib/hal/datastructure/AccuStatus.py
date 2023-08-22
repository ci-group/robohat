from enum import Enum

"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Enum with Accu status constants
"""

class AccuStatus(Enum):
    UNKNOWN = 0
    TOO_LOW = 1
    OK = 2
    TOO_HIGH = 3
    WARNING_2 = 4
    WARNING_1 = 5
    ACCU_NOT_PRESENT = 255
