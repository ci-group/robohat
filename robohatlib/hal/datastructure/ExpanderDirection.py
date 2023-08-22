from enum import Enum

"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Enum with directions for a io expander
"""

class ExpanderDir(Enum):
    OUTPUT = 0
    INPUT = 1
    INVALID = 2