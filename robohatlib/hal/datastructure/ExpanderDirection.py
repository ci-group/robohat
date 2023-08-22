"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Enum with directions for a io expander
"""

try:
    from enum import Enum
except ImportError:
    raise ImportError("Failed to import needed dependencies for ExpanderStatus")

class ExpanderDir(Enum):
    OUTPUT = 0
    INPUT = 1
    INVALID = 2