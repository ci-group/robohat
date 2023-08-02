from enum import Enum

"""!
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
