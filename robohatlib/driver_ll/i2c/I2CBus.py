"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.driver_ll.i2c.I2CHandler import I2CHandler
except ImportError:
    print("Failed to import I2CBus")
    raise

class I2CBus:
    """!
    I2C handler and bus holder
    """

    def __init__(self, _i2c_bus_nr:int, _i2c_handler:I2CHandler):
        """!
        @param _i2c_bus_nr:
        @param _i2c_handler:
        """
        self.__i2c_bus_nr = _i2c_bus_nr
        self.__i2c_handler = _i2c_handler

    # --------------------------------------------------------------------------------------

    def get_i2c_bus_nr(self) -> int:
        """!
        Get i2C bus nr
        @return: bus nr
        """

        return self.__i2c_bus_nr

    # --------------------------------------------------------------------------------------

    def get_i2c_handler(self) -> I2CHandler:
        """
        get I2C handler
        @return: I2CHandler
        """
        return self.__i2c_handler

    # --------------------------------------------------------------------------------------
