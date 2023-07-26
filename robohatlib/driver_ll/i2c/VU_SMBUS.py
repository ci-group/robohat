import posix
from fcntl import ioctl
from ctypes import c_uint32, c_uint8, c_uint16, pointer, POINTER, Structure, Array, Union


# Commands from uapi/linux/i2c-dev.h
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


# ================================================

class i2c_smbus_data(Array):
    """
    Adaptation of the i2c_smbus_data union in ``i2c.h``.

    Data for SMBus messages.
    """
    _length_ = I2C_SMBUS_BLOCK_MAX + 2
    _type_ = c_uint8


class union_i2c_smbus_data(Union):
    _fields_ = [
        ("byte", c_uint8),
        ("word", c_uint16),
        ("block", i2c_smbus_data)
    ]


union_pointer_type = POINTER(union_i2c_smbus_data)

class i2c_smbus_ioctl_data(Structure):

    _fields_ = [
        ('read_write', c_uint8),
        ('command', c_uint8),
        ('size', c_uint32),
        ('data', union_pointer_type)]
    __slots__ = [name for name, type in _fields_]

    @staticmethod
    def create(read_write=I2C_SMBUS_READ, command=0, size=I2C_SMBUS_BYTE_DATA):
        u = union_i2c_smbus_data()

        returnValue = i2c_smbus_ioctl_data(read_write=read_write,
                                           command=command,
                                           size=size,
                                           data=union_pointer_type(u))

        return returnValue

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

class VU_SMBUS():
    __fd = None
    __current_slave_address = None

    #--------------------------------------------------------------------------------------

    def __init__(self, bus=None):
        self.open(bus)

    #--------------------------------------------------------------------------------------

    def open(self, _bus: int) -> None:
        """
        Open SMB bus
        @param _bus:
        @return:
        """
        self.__fd = posix.open("/dev/i2c-{}".format(_bus), posix.O_RDWR)
        self.__current_slave_address = None

        if self.__fd < 0:
            print("Error, failed to open SMB bus")

    #--------------------------------------------------------------------------------------

    def close(self) -> None:
        """
        Close SMB bus
        @return: None
        """
        if self.__fd:
            posix.close(self.__fd)
            self.__fd = None

    #--------------------------------------------------------------------------------------

    def __set_i2c_slave_address(self, _slave_address:int, _force=None) -> None:
        """
        Sets the i2C slave address. Skips if already set

        @param _slave_address: Address of the address i2c slave-device
        @return: None
        """

        if _force is True:
            ioctl(self.__fd, I2C_SLAVE_FORCE, _slave_address & 0x7F)
        else:
            ioctl(self.__fd, I2C_SLAVE, _slave_address & 0x7F)

        self.__current_slave_address = _slave_address

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def write_register_single_byte(self, _slave_address:int, _register, _byte_value) -> None:
        """
        Write a byte value to a register
        @param _slave_address: Address of the address i2c slave-device
        :param _register:
        :param _byte_value:
        :return:
        """

        self.__set_i2c_slave_address(_slave_address)

        msg = i2c_smbus_ioctl_data.create(
                            read_write=I2C_SMBUS_WRITE,
                            command=_register,
                            size=I2C_SMBUS_BYTE_DATA)

        msg.data.contents.byte = _byte_value

        ioctl(self.__fd, I2C_SMBUS, msg)


    def write_register_single_word(self, _slave_address:int, register, value):
        """
        Write a single word (2 bytes) to a given register.

        """
        self.__set_i2c_slave_address(_slave_address)
        msg = i2c_smbus_ioctl_data.create(
                                    read_write=I2C_SMBUS_WRITE,
                                    command=register,
                                    size=I2C_SMBUS_WORD_DATA
                                        )
        msg.data.contents.word = value

        ioctl(self.__fd, I2C_SMBUS, msg)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def write_register_multiple_bytes(self, _slave_address:int, _register, _buffer) -> None:
        """
        Write a block of data to a register
        @param _slave_address: Address of the address i2c slave-device
        @param _register:
        @param _buffer:
        @return: None
        """

        self.__set_i2c_slave_address(_slave_address)

        length = len(_buffer)

        msg = i2c_smbus_ioctl_data.create(
                                    read_write=I2C_SMBUS_WRITE,
                                    command=_register,
                                    size=I2C_SMBUS_BLOCK_DATA)

        msg.data.contents.block[0] = length
        msg.data.contents.block[1:length + 1] = _buffer

        ioctl(self.__fd, I2C_SMBUS, msg)

    #--------------------------------------------------------------------------------------

    def read_single_byte(self, _slave_address:int):
        """
        Read a single data
        @param _slave_address: Address of the address i2c slave-device
        @return: byte data
        """
        return self.read_register_single_byte(_slave_address, 0)

    #--------------------------------------------------------------------------------------

    def read_register_single_byte(self, _slave_address:int, _register):
        """
        @param _slave_address: Address of the address i2c slave-device
        @param _register:
        :return:
        """


        self.__set_i2c_slave_address(_slave_address)

        data_pointer = pointer(c_uint8())

        msg = i2c_smbus_ioctl_data.create(
                                        read_write=I2C_SMBUS_READ,
                                        command=_register,
                                        size=I2C_SMBUS_BYTE_DATA)

        ioctl(self.__fd, I2C_SMBUS, msg)

        return msg.data.contents.byte

    #--------------------------------------------------------------------------------------

    def read_register_multiple_bytes(self, _slave_address:int, _register, _length = I2C_SMBUS_BLOCK_DATA):

        self.__set_i2c_slave_address(_slave_address)

        msg = i2c_smbus_ioctl_data.create(
                                        read_write=I2C_SMBUS_READ,
                                        command=_register,
                                        size=_length)

        ioctl(self.__fd, I2C_SMBUS, msg)

        length = msg.data.contents.block[0]

        return msg.data.contents.block[1:length + 1]

    #--------------------------------------------------------------------------------------

    def transfer_data(self, _slave_address, register, data):

        length = len(data)
        if length > I2C_SMBUS_BLOCK_MAX:
            raise ValueError("Data length cannot exceed %d bytes" % I2C_SMBUS_BLOCK_MAX)

        self.__set_i2c_slave_address(_slave_address)

        msg = i2c_smbus_ioctl_data.create(
                                    read_write=I2C_SMBUS_WRITE,
                                    command=register,
                                    size=I2C_SMBUS_BLOCK_PROC_CALL
                                    )

        msg.data.contents.block[0] = length
        msg.data.contents.block[1:length + 1] = data

        ioctl(self.__fd, I2C_SMBUS, msg)
        length = msg.data.contents.block[0]

        return msg.data.contents.block[1:length + 1]

    #--------------------------------------------------------------------------------------






