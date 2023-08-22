"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

from enum import Enum

"""!
Enum with IO statuses constants
"""

class IOStatus(Enum):
    IO_FAILED = False
    IO_OK = True
