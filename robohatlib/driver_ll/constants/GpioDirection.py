"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

from enum import Enum

"""!
Enum with Gpio direction constants
"""

class GpioDirection(Enum):
    GPIO_OUTPUT = 0
    GPIO_INPUT = 1
