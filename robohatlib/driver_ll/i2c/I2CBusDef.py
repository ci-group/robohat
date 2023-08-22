"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

class I2CBusDef:
    """!
    I2C bus definition
    """

    def __init__(self, _i2_bus_name:str, _i2c_bus_nr:int, _scl_pin:int, _sda_pin:int, _frequency:int=100000):
        """!
        Constructor of I2CBusDef

        @param _i2_bus_name: I2C bus name
        @param _i2c_bus_nr:  I2C bus nr
        @param _scl_pin:  GPIO pin nr of SCL. Must be defined in RPI boot.txt
        @param _sda_pin: GPIO pin nr of SDA. Must be defined in RPI boot.txt
        @param _frequency: frequency of I2C bus (100000 = 100 kHz)
        """

        self.__i2_bus_name = _i2_bus_name
        self.__i2c_bus_nr = _i2c_bus_nr
        self.__scl_pin = _scl_pin
        self.__sda_pin = _sda_pin
        self.__frequency = _frequency

    # --------------------------------------------------------------------------------------

    def get_i2c_bus_name(self) -> str:
        """!
        Get this bus bus_name
        @return: name
        """

        return self.__i2_bus_name

    # --------------------------------------------------------------------------------------

    def get_i2c_bus_nr(self) -> int:
        """!
        Get i2C bus nr
        @return: I2C bus nr
        """

        return self.__i2c_bus_nr

    # --------------------------------------------------------------------------------------

    def get_scl_pin(self) -> int:
        """
        Get this GPIO SCL pin
        @return: SCL
        """

        return self.__scl_pin

    # --------------------------------------------------------------------------------------

    def get_sda_pin(self) -> int:
        """
        Get this GPIO SDA pin
        @return: SDA
        """

        return self.__sda_pin

    # --------------------------------------------------------------------------------------

    def get_frequency(self) -> int:
        """!
        Get current PWM frequency in HX
        @return: frequency
        """

        return self.__frequency

    # --------------------------------------------------------------------------------------