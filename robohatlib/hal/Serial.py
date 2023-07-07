# import serial

# todo not implemented

class Serial:
    # __serialname = ""
    # __serialchannel = 0

    def __init__(self, _iomanager, _serial_def):
        self.__iomanager = _iomanager
        self.__serial_def = _serial_def

    def init_serial(self) -> None:
        """
        Initializes the serial console

        Mandatory

        @return None
        """
        # print("init Serial")
        # ser = serial.Serial(
        #     port='/dev/ttyS0',  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        #     baudrate=9600,
        #     parity=serial.PARITY_NONE,
        #     stopbits=serial.STOPBITS_ONE,
        #     bytesize=serial.EIGHTBITS,
        #     timeout=1
        # )
