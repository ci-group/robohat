"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Data struct to attach properties to an io pin of an IO expander (MCP 23008)
"""

try:
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.constants.GpioDirection import GpioDirection
except ImportError:
    print("Failed to resolve dependencies for McpInitStruct")
    raise


class McpInitStruct:

    def __init__(self, _io_nr: int, _direction=GpioDirection.GPIO_OUTPUT, _interrupt_type=InterruptTypes.INT_NONE) -> None:
        """!
        @param _io_nr:
        @param _direction:
        @param _interrupt_type:
        @return None
        """
        self.__io_nr = _io_nr
        self.__direction = _direction
        self.__interrupt_type = _interrupt_type

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_io_nr(self) -> int:
        """!
        Get io pin nr
        @return: pin nr
        """
        return self.__io_nr

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_direction(self) -> GpioDirection:
        """!
        Get the pin direction of the IO
        @return: GpioDirection
        """
        return self.__direction

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_interrupt_type(self) -> InterruptTypes:
        """!
        Get interrupt type
        @return:
        """
        return self.__interrupt_type

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
