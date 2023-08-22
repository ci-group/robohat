"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

from enum import Enum

"""!
Enum with type of interrupts
"""

class InterruptTypes(Enum):
    INT_NONE = 0
    INT_FALLING = 1
    INT_RISING = 2
    INT_BOTH = 3