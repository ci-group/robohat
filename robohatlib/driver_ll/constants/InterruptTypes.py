from enum import Enum

class InterruptTypes(Enum):
    INT_NONE = 0
    INT_FALLING = 1
    INT_RISING = 2
    INT_BOTH = 3