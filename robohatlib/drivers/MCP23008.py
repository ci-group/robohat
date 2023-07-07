from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
from robohatlib.driver_ll.constants.GPIO_Direction import GpioDirection

try:
    from robohatlib.helpers.RoboUtil import RoboUtil
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
except ImportError:
    print("Failed to import RoboUtil")
    raise

IODIR_ADDRESS =     0x00
IPOL_ADDRESS =      0x01
GPINTEN_ADDRESS =   0x02
DEFVAL_ADDRESS =    0x03
INTCON_ADDRESS =    0x04
IOCON_ADDRESS =     0x05
GPPU_ADDRESS =      0x06
INTF_ADDRESS =      0x07
INTCAP_ADDRESS =    0x08
GPIO_ADDRESS =      0x09

INTPOL_BITNR =      1


class MCP23008:
    def __init__(self, _i2cdevice, _mcp_interruptdefinition):
        self.__i2cdevice = _i2cdevice
        self.__mcp_interruptdefinition = _mcp_interruptdefinition

    # --------------------------------------------------------------------------------------
    def init_MCP23008(self):

        print("init_MCP23008")

        self.__i2cdevice.i2c_write_register_byte(0x00, 0x00)        # empty data, wake up mcp
        self.invert_port(0x00)
        self.set_interrupt_polarity(True)

        # self.set_port_direction(0xff)
        # self.set_port_pullup(0xFF)
        # self.set_interrupt_on_port(0xff )
        # self.set_interrupt_type_port(0x00 )

        #self.reset_interrupts()

        if self.__mcp_interruptdefinition is not None:
            iodir_value = 0x00
            gpinten_value = 0x00
            intcon_value = 0x00
            defval_value = 0x00


            servoassembly_interupt_settings_array = self.__mcp_interruptdefinition.get_interrupt_settings()
            for servoassembly_interupt_settings in servoassembly_interupt_settings_array:
                bitnr = servoassembly_interupt_settings.get_io_nr()
                if servoassembly_interupt_settings.get_direction is GpioDirection.GPIO_OUTPUT:
                    iodir_value = RoboUtil.updatebyte(iodir_value, bitnr, 0)                                    # direction output
                else:

                    iodir_value = RoboUtil.updatebyte(iodir_value, bitnr, 1)                                    # direction input
                    if servoassembly_interupt_settings.get_interrupt_type() is InterruptTypes.INT_NONE:
                        gpinten_value = RoboUtil.updatebyte(gpinten_value, bitnr, 0)                            # disables int
                    else:
                        gpinten_value = RoboUtil.updatebyte(gpinten_value, bitnr, 1)                            # enables int
                        if servoassembly_interupt_settings.get_interrupt_type() is InterruptTypes.INT_RISING:
                            intcon_value = RoboUtil.updatebyte(intcon_value, bitnr, 0)                          # compare with defval value
                            defval_value = RoboUtil.updatebyte(defval_value, bitnr, 0)                          # int if pin goes from 0 to 1 int occurs
                        elif servoassembly_interupt_settings.get_interrupt_type() is InterruptTypes.INT_FALLING:
                            intcon_value = RoboUtil.updatebyte(intcon_value, bitnr, 0)                          # compare with defval value
                            defval_value = RoboUtil.updatebyte(defval_value, bitnr, 1)                          # int if pin goes from 1 to 0 int occurs
                        else:                                                                                   # BOTH
                            intcon_value = RoboUtil.updatebyte(intcon_value, bitnr, 1)                          # int when pin changes
                            defval_value = RoboUtil.updatebyte(defval_value, bitnr, 1)                          # DOES NOT CARE

            self.set_port_direction( iodir_value )
            self.set_port_pullup(0xFF)
            self.set_interrupt_on_port( gpinten_value )
            self.set_interrupt_type_port( intcon_value )
            self.set_interrupt_defaults(defval_value)
        self.reset_interrupts()

    # --------------------------------------------------------------------------------------
    def set_pin_direction(self, _ionr, _direction):
        self.__set_pin(IODIR_ADDRESS, _ionr, _direction)

    def get_pin_direction(self, _ionr):
        return self.__get_pin(IODIR_ADDRESS, _ionr)

    def set_port_direction(self, _bytevalue):
        print("port direction: " + hex(_bytevalue))
        self.__set_port(IODIR_ADDRESS, _bytevalue)

    def get_port_direction(self):
        return self.__get_port(IODIR_ADDRESS)

    def set_pin_pullup(self, _ionr, _boolvalue):
        self.__set_pin(GPPU_ADDRESS, _ionr, _boolvalue)
        return

    def get_pin_pullup(self, _ionr):
        return self.__get_pin(GPPU_ADDRESS, _ionr)

    def set_port_pullup(self, _bytevalue):
        print("port pullup: " + hex(_bytevalue))
        self.__set_port(GPPU_ADDRESS, _bytevalue)

    def set_pin_data(self, _ionr, _boolvalue):
        self.__set_pin(GPIO_ADDRESS, _ionr, _boolvalue)
        return

    def get_pin_data(self, _io_nr):
        """!
        get the input status of an io pin of the IO expander

        Note. direction of the pin must be an Input

        @param _io_nr io nr

        @return status of the pin
        """

        return self.__get_pin(GPIO_ADDRESS, _io_nr)

    def set_port_data(self, _bytevalue):
        self.__set_port(GPIO_ADDRESS, _bytevalue)
        return

    def get_port_data(self):
        return self.__get_port(GPIO_ADDRESS)

    def invert_pin(self, _pinnr, _boolvalue):
        self.__set_pin(IPOL_ADDRESS, _pinnr, _boolvalue)
        return

    def get_pin_polarity(self, _pinnr):
        return self.__get_pin(IPOL_ADDRESS, _pinnr)

    def invert_port(self, _bytevalue):
        self.__set_port(IPOL_ADDRESS, _bytevalue)
        return

    def get_port_polarity(self):
        return self.__get_port(IPOL_ADDRESS)

#----------------------------------------------------------

    def set_interrupt_polarity(self, _boolvalue):
        conf = self.__i2cdevice.i2c_read_register_byte(IOCON_ADDRESS)
        self.__i2cdevice.i2c_write_register_byte(IOCON_ADDRESS, RoboUtil.updatebyte(conf, INTPOL_BITNR, _boolvalue))
        return

    def get_interrupt_polarity(self):
        return RoboUtil.checkbit(self.__i2cdevice.i2c_read_register_byte(INTCON_ADDRESS), INTPOL_BITNR)

    def set_interrupt_type_port(self, _bytevalue):
        self.__set_port(INTCON_ADDRESS, _bytevalue)
        return

    def get_interrupt_type(self):
        return self.__get_port(INTCON_ADDRESS)

    def set_interrupt_defaults(self, _bytevalue):
        self.__set_port(DEFVAL_ADDRESS, _bytevalue)
        return

    def get_interrupt_defaults(self):
        return self.__get_port(DEFVAL_ADDRESS)

    def set_interrupt_on_pin(self, _pinnr, _boolvalue):
        self.__set_pin(DEFVAL_ADDRESS, _pinnr, _boolvalue)
        return

    def get_interrupt_on_pin(self, _pinnr):
        return self.__get_pin(GPINTEN_ADDRESS, _pinnr)

    def set_interrupt_on_port(self, _bytevalue):
        self.__set_port(GPINTEN_ADDRESS, _bytevalue)
        return

    def get_interrupt_on_port(self):
        return self.__get_port(GPINTEN_ADDRESS)

    def read_interrupt_status(self):
        return self.__get_port(INTF_ADDRESS)

    def read_interrupt_capture(self):
        return self.__get_port(INTCAP_ADDRESS)

    def reset_interrupts(self):
        tmp = self.read_interrupt_capture()
        del tmp

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __set_pin(self, _register, _ionr, _wantedpinvalue):
        self.__checkIfExpanderIOisAvailble(_ionr)

        if _wantedpinvalue < 0 or _wantedpinvalue > 1:
            raise ValueError("value out of range: 0 or 1")

        curval = self.__i2cdevice.i2c_read_register_byte(_register)
        newval = RoboUtil.updatebyte(curval, _ionr, _wantedpinvalue)

        self.__i2cdevice.i2c_write_register_byte(_register, newval)
        return

    #--------------------------------------------------------------------------------------

    def __get_pin(self, _register, _ionr):
        self.__checkIfExpanderIOisAvailble(_ionr)

        curval = self.__i2cdevice.i2c_read_register_byte(_register)
        return  RoboUtil.checkbit(curval, _ionr) # - 1)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __set_port(self, _register, _value):
        if _value < 0 or _value > 0xFF:
            raise ValueError("value out of range: 0 to 255 --> " + hex(_value))

        self.__i2cdevice.i2c_write_register_byte(_register, _value)
        return

    #--------------------------------------------------------------------------------------
    def __get_port(self, _register):
        return self.__i2cdevice.i2c_read_register_byte(_register)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __checkIfExpanderIOisAvailble(self, _io_nr) -> None:
        if _io_nr not in range(0, 8):
            raise ValueError("only io0 till io7 are available")
