"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Enum with statuses for a io expander
"""

try:
    from enum import Enum
except ImportError:
    raise ImportError("Failed to import needed dependencies for ExpanderStatus")

class ExpanderStatus(Enum):
    LOW = 0
    HIGH = 1
    INVALID = 2