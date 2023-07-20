from enum import Enum

"""!
Enum with directions for a io expander
"""

class ExpanderDir(Enum):
    OUTPUT = 0
    INPUT = 1
    INVALID = 2