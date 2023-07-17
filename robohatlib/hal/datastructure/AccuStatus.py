from enum import Enum
class AccuStatus(Enum):
    UNKNOWN = 0
    TOO_LOW = 1
    OK = 2
    TOO_HIGH = 3
    ACCU_NOT_PRESENT = 4
