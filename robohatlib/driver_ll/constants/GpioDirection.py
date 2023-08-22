"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Enum with Gpio direction constants
"""

from enum import Enum

class GpioDirection(Enum):
    GPIO_OUTPUT = 0
    GPIO_INPUT = 1
