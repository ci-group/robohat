try:
    from robohatlib.driver_ll.i2c.I2CHandler import I2CHandler
except ImportError:
    print("Failed to import I2CDevice")
    raise

class I2CDevice:
    """!
    I2C device
    """

    def __init__(self, _device_name:str, _i2c_handler:I2CHandler, _i2c_bus_nr:int, _i2c_device_address:int):
        """!
        @param _device_name:
        @param _i2c_handler:
        @param _i2c_bus_nr:
        @param _i2c_device_address:
        """
        self.__device_name = _device_name
        self.__i2c_handler = _i2c_handler
        self.__i2c_bus_nr = _i2c_bus_nr
        self.__i2c_device_address = _i2c_device_address

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def i2c_write_register_byte(self, _register, _value) -> None:
        """!
        Writes a byte to a register
        @param _register:
        @param _value:
        @return: None
        """
        while not self.__i2c_handler.try_lock():
            try:
                self.__i2c_handler.write_to(self.__i2c_device_address, bytes([_register, _value]))
            finally:
                self.__i2c_handler.unlock()


    def i2c_write_bytes(self, _value_bytes: []) -> None:
        """!
        Writes bytes to a register
        @param _value_bytes:
        @return: None
        """

        while not self.__i2c_handler.try_lock():
            try:
                self.__i2c_handler.write_to(self.__i2c_device_address, _value_bytes)
            finally:
                self.__i2c_handler.unlock()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def i2c_read_register_byte(self, _register):
        """!
        @param _register:
        @return: byte
        """
        return_value_array = bytearray(1)
        while not self.__i2c_handler.try_lock():
            try:
                self.__i2c_handler.write_to_then_read_from(self.__i2c_device_address, bytes([_register]), return_value_array)
            finally:
                self.__i2c_handler.unlock()

        return return_value_array[0]

    #--------------------------------------------------------------------------------------

    def read_from_into(self, _bytes_out) -> None:
        """
        @param _bytes_out: buffer to store data read from i2c device
        @return: None
        """
        while not self.__i2c_handler.try_lock():
            try:
                self.__i2c_handler.read_from_into(self.__i2c_device_address, _bytes_out)
            finally:
                self.__i2c_handler.unlock()



    def write_to_then_read_from(self, _bytes_to, _bytes_out):
        """
        @param _bytes_to: data to I2C device
        @param _bytes_out: buffer to store data read from i2c device
        @return: None
        """
        while not self.__i2c_handler.try_lock():
            try:
                self.__i2c_handler.write_to_then_read_from(self.__i2c_device_address, _bytes_to, _bytes_out)
            finally:
                self.__i2c_handler.unlock()


    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_device_name(self) -> str:
        """!
        Get device name
        :return: name
        """
        return self.__device_name

    def get_i2c_bus_nr(self) -> int:
        """!
        Get bus nr
        @return: bus nr
        """
        return self.__i2c_bus_nr

    def get_i2c_device_address(self) -> int:
        """!
        Get device address
        @return: i2c_device_address
        """
        return self.__i2c_device_address

    def get_i2c_handler(self) -> I2CHandler:
        """!
        Get i2c handler
        @return: i2c handler
        """
        return self.__i2c_handler

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------