"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Enum with Gpio status constants
"""

from enum import Enum

class GPOStat(Enum):
    GPO_LOW = 0
    GPO_HIGH = 1