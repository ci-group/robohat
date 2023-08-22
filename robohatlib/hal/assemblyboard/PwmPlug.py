"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

PWM plug enum
"""

try:
    from enum import Enum
except ImportError:
    raise ImportError("Failed to import needed dependencies for ExpanderStatus")

class PwmPlug(Enum):
    PWMPLUG_P3 = 0
    PWMPLUG_P4 = 1