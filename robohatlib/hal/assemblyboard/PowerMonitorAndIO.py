
try:
    from robohatlib.drivers.MCP23008 import MCP23008
except ImportError:
    print("Failed to import MCP23008")
    raise

from robohatlib.hal.datastructure.ExpanderDirection import ExpanderDir


class POWERMONITORANDIO:
    def __init__(self, _i2cdevice, _mcp_interruptdefinition=None):
        self.__iodevice = MCP23008(_i2cdevice, _mcp_interruptdefinition)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def init_powermonitor(self):
        print("init_powermonitor")

    def is_power_good(self, _powerchannel):
        return True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def set_direction_ioexpander(self, _ionr, _direction):        # 0 = Pin is configured as an output, 1 = Pin is configured as an input
        self.__checkIfExpanderIOisAvailble(_ionr)

        if _direction is ExpanderDir.OUTPUT:
            wantedpinvalue = 0
        else:
            wantedpinvalue = 1
        self.__iodevice.set_pin_direction(_ionr, wantedpinvalue)

    # --------------------------------------------------------------------------------------


    def set_ouput_ioexpander(self, _ionr, _boolvalue):
        self.__checkIfExpanderIOisAvailble(_ionr)

        self.__iodevice.set_pin_data(_ionr, _boolvalue)

    # --------------------------------------------------------------------------------------

    def get_input_ioexpander(self, _ionr):
        self.__checkIfExpanderIOisAvailble(_ionr)

        return self.__iodevice.get_pin_data(_ionr)

    # --------------------------------------------------------------------------------------

    def __checkIfExpanderIOisAvailble(self, _ionr):
        if _ionr not in range(4, 7):
            raise ValueError("only io4, io5 and io6 are availble")