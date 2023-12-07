"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.driver_ll.i2c.I2CHandler import I2CHandler
    import time
except ImportError:
    print("Failed to import I2CDevice")
    raise

class I2CDevice:
    """!
    I2C device
    """

    def __init__(self, _device_name: str, _i2c_handler: I2CHandler, _i2c_bus_nr: int, _i2c_device_address: int):
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

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    #OK
    def i2c_write_register_byte(self, _register, _value) -> None:
        """!
        Writes a byte to a register
        @param _register:
        @param _value:
        @return: None
        """
        self.i2c_write_bytes(bytes([_register, _value]))

    # --------------------------------------------------------------------------------------
    #OK
    def i2c_write_bytes(self, _value_bytes: []) -> None:
        """!
        Writes bytes to a register
        @param _value_bytes:
        @return: None
        """

        self.__i2c_handler.wait_until_unlocked()

        try:
            self.__i2c_handler.write_bytes(self.__i2c_device_address, _value_bytes)
        finally:
            self.__i2c_handler.unlock()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # OK
    def i2c_read_register_byte(self, _register):
        """!
        @param _register:
        @return: byte
        """
        return_value_array = bytearray(1)

        self.__i2c_handler.wait_until_unlocked()

        try:
            self.__i2c_handler.write_to_then_read_from(self.__i2c_device_address, bytes([_register]), return_value_array)
        finally:
            self.__i2c_handler.unlock()

        return return_value_array[0]

    # --------------------------------------------------------------------------------------
    #OK
    def i2c_read_register_multiple_bytes(self, _register, _bytes_out_buffer):
        """!
        Read multiple bytes from register
        @param _register:
        @param _bytes_out_buffer:
        @return:
        """
        in_value_array = bytearray(1)
        in_value_array[0] = _register

        self.write_to_then_read_from(in_value_array, _bytes_out_buffer)

    # --------------------------------------------------------------------------------------
    #OK
    def read_from_into(self, _bytes_out) -> None:
        """!
        @param _bytes_out: buffer to store data read from i2c device
        @return: None
        """
        self.__i2c_handler.wait_until_unlocked()

        try:
            self.__i2c_handler.read_from_into(self.__i2c_device_address, _bytes_out)
        finally:
            self.__i2c_handler.unlock()

    # --------------------------------------------------------------------------------------
    #OK
    def write_to_then_read_from(self, _bytes_to, _bytes_out):
        """!
        @param _bytes_to: data to I2C device
        @param _bytes_out: buffer to store data read from i2c device
        @return: None
        """
        self.__i2c_handler.wait_until_unlocked()

        try:
            self.__i2c_handler.write_to_then_read_from(self.__i2c_device_address, _bytes_to, _bytes_out)
        finally:
            self.__i2c_handler.unlock()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_device_name(self) -> str:
        """!
        Get device_name
        @return: str
        """
        return self.__device_name

    def get_i2c_bus_nr(self) -> int:
        """!
        Get the i2c bus_nr
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

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------