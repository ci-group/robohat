class I2CDeviceDef:
    """!
    Definition of an I2C device
    """

    def __init__(self, _name:str, _i2c_bus_nr:int, _i2c_base_address:int, _i2c_offset_address=0):
        """!
        @param _name: name of this definition
        @param _i2c_bus_nr: I2C bus nr
        @param _i2c_base_address: I2C base address
        @param _i2c_offset_address:  I2C offset address
        """
        self.__name = _name
        self.__i2c_bus_nr = _i2c_bus_nr
        self.__i2c_base_address = _i2c_base_address
        self.__i2c_offset_address = _i2c_offset_address

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Get name of this definition
        @return: name
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_i2c_bus_nr(self) -> int:
        """!
        Get I2C bus nr
        @return: I2C bus nr
        """
        return self.__i2c_bus_nr

    # --------------------------------------------------------------------------------------

    def get_i2c_device_address(self) -> int:
        """!
        Get I2C device address (actual base address + offset address)
        @:return: I2C device address
        """
        return self.__i2c_base_address + self.__i2c_offset_address

    # --------------------------------------------------------------------------------------

    def get_i2c_base_address(self) ->int:
        """!
        Get I2C base address
        @:return: I2C base address
        """
        return self.__i2c_base_address

    # --------------------------------------------------------------------------------------

    def get_i2c_offset_address(self) -> int:
        """!
        Get I2C offset address
        @:return: I2C offset
        """
        return self.__i2c_offset_address

    def set_i2c_offset_address(self, _i2c_offset_address:int) -> None:
        """!
        Set new I2C offset address
        @param _i2c_offset_address:
        @return: None
        """
        self.__i2c_offset_address = _i2c_offset_address

    # --------------------------------------------------------------------------------------