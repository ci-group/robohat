"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from fcntl import ioctl
    from ctypes import c_uint32, c_uint8, c_uint16, pointer, POINTER, Structure, Array, Union
except ImportError:
    print("Failed to resolve dependencies for the SMMbus")
    raise


# Commands from uapi/linux/i2c-dev.h for use with ioctl

I2C_RETRIES	= 0x0701        #number of times a device address should be polled when not acknowledging
I2C_TIMEOUT	= 0x0702        # set timeout - call with int
I2C_SLAVE = 0x0703          # Change slave address, Slave address is 7 or 10 bits
I2C_SLAVE_FORCE = 0x0706    # Change slave address, Slave address is 7 or 10 bits  This changes the address, even if it is already taken!
I2C_TENBIT = 0x0704         # 0 for 7 bit addrs, != 0 for 10 bit
I2C_FUNCS = 0x0705          # Get the adapter functionality
I2C_RDWR = 0x0707           # Combined R/W transfer (one stop only)
I2C_PEC = 0x0708            # != 0 to use PEC with SMBus
I2C_SMBUS = 0x0720          # SMBus-level access

I2C_M_RD = 0x0001           # read data, from slave to master
I2C_M_TEN = 0x0010          # we have a ten bit chip address
I2C_M_RECV_LEN = 0x0400     #
I2C_M_NO_RD_ACK = 0x0800    #
I2C_M_IGNORE_NAK = 0x1000   #
I2C_M_REV_DIR_ADDR = 0x2000 #
I2C_M_NOSTART = 0x4000      #
I2C_M_STOP = 0x8000         #

# SMBus transfer read or write markers from uapi/linux/i2c.h
I2C_SMBUS_WRITE = 0
I2C_SMBUS_READ = 1

# Size identifiers uapi/linux/i2c.h
I2C_SMBUS_QUICK	= 0
I2C_SMBUS_BYTE = 1
I2C_SMBUS_BYTE_DATA = 2
I2C_SMBUS_WORD_DATA = 3
I2C_SMBUS_PROC_CALL = 4
I2C_SMBUS_BLOCK_DATA = 5
I2C_SMBUS_I2C_BLOCK_DATA = 6
I2C_SMBUS_BLOCK_PROC_CALL = 7

# Pointer definitions
LP_c_uint8 = POINTER(c_uint8)
LP_c_uint16 = POINTER(c_uint16)
LP_c_uint32 = POINTER(c_uint32)

I2C_SMBUS_BLOCK_MAX = 32


# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class SMBUS:
    """!
    Class which is the bridge between i2c and the linux hardware
    """
    def __init__(self, _bus_nr: int):
        """!
        Constructor

        @param _bus_nr: bus nr off the i2C. note... bus nr should be present in device.txt in boo of rpi
        Constructor if this SMBbus
        @param _bus_nr:
        """

        self.__device = None
        self.__open(_bus_nr)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __del__(self):
        """!
        Descructor

        Destructor if this SMBbus
        """
        self.__close()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __open(self, _bus_nr: int) -> None:
        """!
        Open the SMBbus
        @param _bus_nr the bus nr of the used I2C
        @return: None
        """

        # already opened by the user
        if self.__device is not None:
            return

        self.__device = open("/dev/i2c-{0}".format(_bus_nr), "r+b", buffering=0)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __close(self) -> None:
        """!
        Close the SMBbus
        @return: None
        """

        if self.__device is not None:
            self.__device.close()
            self.__device = None

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __set_i2c_slave_address(self, _slave_address, _force=None) -> bool:
        """!
        Sets the i2C slave address. If OK, it returns True

        @param _slave_address: Address of the address i2c slave-device
        @param _force. Used linux call with the force parameter
        @return: bool
        """
        if self.__device is None:
            return False

        if _force is True:
            status = ioctl(self.__device.fileno(), I2C_SLAVE_FORCE, _slave_address & 0x7F)
        else:
            status = ioctl(self.__device.fileno(), I2C_SLAVE, _slave_address & 0x7F)

        self.__current_slave_address = _slave_address

        if status < 1:
            return False
        else:
            return True

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def read_byte(self, _slave_address):
        """!
        Read a single byte from the SMB bus
        @param _slave_address:
        @return: 1 byte
        """
        self.__set_i2c_slave_address(_slave_address)
        return ord(self.__device.read(1))

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #OK
    def read_bytes(self, _slave_address, _size_of_bytes_to_read) -> bytes:
        """!
        Reads multiple bytes from the SMB bus
        @param _slave_address:
        @param _size_of_bytes_to_read
        @return: bytes
        """
        self.__set_i2c_slave_address(_slave_address)
        return self.__device.read(_size_of_bytes_to_read)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def write_byte(self, _slave_address, _byte_value) -> None:
        """!
        Write a byte to the I2C bus
        @param _slave_address:
        @param _byte_value:
        @return:
        """

        data = bytearray(1)
        data[0] = _byte_value & 0xFF
        self.write_bytes(_slave_address, data)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def write_bytes(self, _slave_address, _buffer_out) -> None:
        """
        Writes multiple bytes to the I2C bus
        @param _slave_address:
        @param _buffer_out:
        @return: None
        """

        self.__set_i2c_slave_address(_slave_address)
        self.__device.write(_buffer_out)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

