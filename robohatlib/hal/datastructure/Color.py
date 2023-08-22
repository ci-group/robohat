"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Enum with Colors for a LED
"""

try:
    from enum import Enum
except ImportError:
    raise ImportError("Failed to import needed dependencies for ExpanderStatus")

class Color(Enum):
    NONE = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5
    PURPLE = 6
    OFF = 254
    ON = 255