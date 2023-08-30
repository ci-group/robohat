"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Driver for the MCP23008
The MCP23008 is a 8 bit I/O expander controlled by I2C

Needed is the connected I2C-bus
An interrupt definition is not mandatory, but when the definition is not present the interrupt will be disabled
"""

try:
    from robohatlib.helpers.RoboUtil import RoboUtil
    from robohatlib.RobohatConfig import DEBUG
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.constants.GpioDirection import GpioDirection
except ImportError:
    print("Failed to resolve dependencies for MCP23008")
    raise

IO_DIR_ADDRESS =        0x00
IPOL_ADDRESS =          0x01
GP_INT_EN_ADDRESS =     0x02
DEF_VAL_ADDRESS =       0x03
INT_CON_ADDRESS =       0x04
IO_CON_ADDRESS =        0x05
GP_PU_ADDRESS =         0x06
INTF_ADDRESS =          0x07
INT_CAP_ADDRESS =       0x08
GPIO_ADDRESS =          0x09

INT_POL_BIT_NR =        1

class MCP23008:
    """!
    Constructor MCP23008
    """
    def __init__(self, _i2c_device: I2CDevice, _mcp_interrupt_definition: [] = None):
        self.__i2c_device = _i2c_device
        self.__mcp_interrupt_definition = _mcp_interrupt_definition

    # --------------------------------------------------------------------------------------
    def init_mcp23008(self):
        """!
        Initializes the MCP23008

        @return -> None:
        """

        self.__i2c_device.i2c_write_register_byte(0x00, 0x00)        # empty data, wake up mcp
        self.invert_port(0x00)
        self.set_interrupt_polarity(True)

        if self.__mcp_interrupt_definition is not None:
            io_dir_value = 0x00
            gp_int_en_value = 0x00
            int_con_value = 0x00
            def_val_value = 0x00

            interrupt_settings_list = self.__mcp_interrupt_definition.get_interrupt_settings()
            for interrupt_settings in interrupt_settings_list:
                bit_nr = interrupt_settings.get_io_nr()
                if interrupt_settings.get_direction is GpioDirection.GPIO_OUTPUT:
                    io_dir_value = RoboUtil.update_byte(io_dir_value, bit_nr, 0)                                    # direction output
                else:
                    io_dir_value = RoboUtil.update_byte(io_dir_value, bit_nr, 1)                                    # direction input
                    if interrupt_settings.get_interrupt_type() is InterruptTypes.INT_NONE:
                        gp_int_en_value = RoboUtil.update_byte(gp_int_en_value, bit_nr, 0)                          # disables int
                    else:
                        gp_int_en_value = RoboUtil.update_byte(gp_int_en_value, bit_nr, 1)                          # enables int
                        if interrupt_settings.get_interrupt_type() is InterruptTypes.INT_RISING:
                            int_con_value = RoboUtil.update_byte(int_con_value, bit_nr, 0)                          # compare with def_val value
                            def_val_value = RoboUtil.update_byte(def_val_value, bit_nr, 0)                          # int if pin goes from 0 to 1 int occurs
                        elif interrupt_settings.get_interrupt_type() is InterruptTypes.INT_FALLING:
                            int_con_value = RoboUtil.update_byte(int_con_value, bit_nr, 0)                          # compare with def_val value
                            def_val_value = RoboUtil.update_byte(def_val_value, bit_nr, 1)                          # int if pin goes from 1 to 0 int occurs
                        else:                                                                                      # BOTH
                            int_con_value = RoboUtil.update_byte(int_con_value, bit_nr, 1)                          # int when pin changes
                            def_val_value = RoboUtil.update_byte(def_val_value, bit_nr, 1)                          # DOES NOT CARE

            self.set_port_direction(io_dir_value )
            self.set_port_pullup(0xFF)
            self.set_interrupt_on_change_port(gp_int_en_value)
            self.set_interrupt_type_port( int_con_value )
            self.set_interrupt_defaults(def_val_value)
        else:
            self.set_port_direction(0xff)
            self.set_port_pullup(0xFF)

        self.reset_interrupts()

    # --------------------------------------------------------------------------------------
    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down
        @return: None
        """
        self.set_port_direction(0xff)           # set all input

    # --------------------------------------------------------------------------------------
    def set_pin_direction(self, _io_nr:int, _direction) -> None:
        """!
        set the direction of a I/O pin.
        @param _direction The direction 0 or 1:  1 to a pin is input, 0 is output.
        @param _io_nr: I/O pin nr: 0 - 7
        @return: None
        """

        if DEBUG is True:
            print("Setting pin direction: " + str(_io_nr) + " " + str(_io_nr) )
        self.__set_pin(IO_DIR_ADDRESS, _io_nr, _direction)

    def get_pin_direction(self, _io_nr: int):
        """!
        Get the direction of a I/O pins. 1 to a pin is input.
        @param _io_nr: I/O pin nr: 0 - 7
        @return: int, pin direction
        """
        return self.__get_pin(IO_DIR_ADDRESS, _io_nr)

    def set_port_direction(self, _byte_value) -> None:
        """!
        Set the direction of all the 8 I/O pins. 1 to a pin is input. So 0xff is all input
        @param _byte_value:
        @return: None
        """
        self.__set_port(IO_DIR_ADDRESS, _byte_value)

    def get_port_direction(self):
        """!
        Get the direction of all the 8 I/O pins. 1 to a pin is input. So 0xff is all input
        @return: None
        """
        return self.__get_port(IO_DIR_ADDRESS)
    # --------------------------------------------------------------------------------------
    def set_pin_pullup(self, _io_nr:int, _bool_value) -> None:
        """!
        Set pull up of a pin
        @param _io_nr:
        @param _bool_value:
        @return:  None
        """
        self.__set_pin(GP_PU_ADDRESS, _io_nr, _bool_value)
        return

    def get_pin_pullup(self, _io_nr:int) -> int:
        return self.__get_pin(GP_PU_ADDRESS, _io_nr)

    def set_port_pullup(self, _byte_value):
        self.__set_port(GP_PU_ADDRESS, _byte_value)

    def set_pin_data(self, _io_nr: int, _bool_value) -> None:
        self.__set_pin(GPIO_ADDRESS, _io_nr, _bool_value)
        return

    def get_pin_data(self, _io_nr: int):
        """!
        get the input status of an io pin of the IO expander
        Note. direction of the pin must be an Input

        @param _io_nr io nr
        @return status of the pin
        """

        return self.__get_pin(GPIO_ADDRESS, _io_nr)

    def set_port_data(self, _byte_value) -> None:
        self.__set_port(GPIO_ADDRESS, _byte_value)
        return

    def get_port_data(self):
        return self.__get_port(GPIO_ADDRESS)

    def invert_pin(self, _pin_nr:int, _bool_value) -> None:
        self.__set_pin(IPOL_ADDRESS, _pin_nr, _bool_value)
        return

    def get_pin_polarity(self, _pin_nr: int):
        return self.__get_pin(IPOL_ADDRESS, _pin_nr)

    def invert_port(self, _bool_value) -> None:
        self.__set_port(IPOL_ADDRESS, _bool_value)
        return

    def get_port_polarity(self):
        return self.__get_port(IPOL_ADDRESS)

#----------------------------------------------------------

    def set_interrupt_polarity(self, _bool_value) -> None:
        conf = self.__i2c_device.i2c_read_register_byte(IO_CON_ADDRESS)
        self.__i2c_device.i2c_write_register_byte(IO_CON_ADDRESS, RoboUtil.update_byte(conf, INT_POL_BIT_NR, _bool_value))
        return

    def get_interrupt_polarity(self):
        return RoboUtil.check_bit(self.__i2c_device.i2c_read_register_byte(INT_CON_ADDRESS), INT_POL_BIT_NR)

    def set_interrupt_type_port(self, _byte_value):
        self.__set_port(INT_CON_ADDRESS, _byte_value)
        return

    def get_interrupt_type(self):
        return self.__get_port(INT_CON_ADDRESS)

    def set_interrupt_defaults(self, _byte_value) -> None:
        self.__set_port(DEF_VAL_ADDRESS, _byte_value)
        return

    def get_interrupt_defaults(self):
        return self.__get_port(DEF_VAL_ADDRESS)

    def set_interrupt_on_pin(self, _pin_nr: int, _bool_value) -> None:
        self.__set_pin(DEF_VAL_ADDRESS, _pin_nr, _bool_value)
        return

    def get_interrupt_on_change_pin(self, _pin_nr: int):
        """!
        get status if pin is enable or disable interrupt on change
        @param _pin_nr:
        @return: 1 interrupt on change is enabled, or 0 interrupt on change is disabled
        """
        return self.__get_pin(GP_INT_EN_ADDRESS, _pin_nr)

    def set_interrupt_on_change_port(self, _byte_value) -> None:
        """!
        Enable or disable interrupt on change (not this is a port, so all 8 I/O)
        @param _byte_value: value to set
        @return: None
        """
        self.__set_port(GP_INT_EN_ADDRESS, _byte_value)
        return

    def get_interrupt_on_change_port(self):
        """!
        Get Enable or disable interrupt on change (not this is a port, so all 8 I/O)
        @return: 1 interrupt on change is enabled, or 0 interrupt on change is disabled So 0xFF all are enabled
        """
        return self.__get_port(GP_INT_EN_ADDRESS)

    def read_interrupt_status(self):
        return self.__get_port(INTF_ADDRESS)

    def read_interrupt_capture(self):
        return self.__get_port(INT_CAP_ADDRESS)

    def reset_interrupts(self):
        self.read_interrupt_capture()


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __set_pin(self, _register, _io_nr:int, _wanted_pin_value) -> None:

        if self.__check_if_expander_io_is_available(_io_nr) is True:
            if _wanted_pin_value < 0 or _wanted_pin_value > 1:
                raise ValueError("value out of range: 0 or 1")

            cur_val = self.__i2c_device.i2c_read_register_byte(_register)
            new_val = RoboUtil.update_byte(cur_val, _io_nr, _wanted_pin_value)

            self.__i2c_device.i2c_write_register_byte(_register, new_val)
        else:
            print("pin " + str(_io_nr) + " doesn't exist")

    #--------------------------------------------------------------------------------------

    def __get_pin(self, _register, _io_nr) -> int:
        if self.__check_if_expander_io_is_available(_io_nr) is True:
            cur_val = self.__i2c_device.i2c_read_register_byte(_register)
            return  RoboUtil.check_bit(cur_val, _io_nr) # - 1)
        else:
            print("pin " + str(_io_nr) + " doesn't exist")

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __set_port(self, _register, _value) -> None:
        if _value < 0 or _value > 0xFF:
            raise ValueError("value out of range: 0 to 255 --> " + hex(_value))

        self.__i2c_device.i2c_write_register_byte(_register, _value)
        return

    #--------------------------------------------------------------------------------------
    def __get_port(self, _register):
        """!
        Gives port value (byte)
        @param _register:
        @return: port value
        """
        return self.__i2c_device.i2c_read_register_byte(_register)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    # noinspection PyMethodMayBeStatic
    def __check_if_expander_io_is_available(self, _io_nr) -> bool:
        """!
        Return True when _io_nr is in range
        @param _io_nr: the io nr
        @return: bool
        """
        if _io_nr in range(0, 8):
            return True
        return False

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------