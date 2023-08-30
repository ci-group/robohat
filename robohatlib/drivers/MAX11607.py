"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Driver for the MAX11607
The MAX11607 is an ADC, 4 channel, 10 bit controlled by I2C

Needed is the connected I2C-bus
"""

try:
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
except ImportError:
    print("Failed to import MAX11607")
    raise

class MAX11607:
    # --------------------------------------------------------------------------------------
    def __init__(self, _i2c_device:I2CDevice):
        """!
        Constructor
        @param _i2c_device:
        """

        self.__i2c_device = _i2c_device

        self.__adc_max_count = 1024
        self.__adc_ref_voltage = 3.3
        self.__adc_result_voltage = [0.0] * 4  # allocates and fills alle elements of list with 0


    # --------------------------------------------------------------------------------------
    def init_adc(self) -> None:
        """
        Initializes the ADC
        @return: None
        """


        register_data = 0x80 | 0x2                                              # aak default, no reset
        conf_data = 0x01 | 0x06                                                 # single ended, multiple channel (0 un till last), last channel is AIN3 (channel 4)

        self.__i2c_device.i2c_write_register_byte(register_data, conf_data)
        #self.__i2c_device.i2c_write_bytes(bytes([register_data, conf_data]))

    # self.device.readinto(result)
    # --------------------------------------------------------------------------------------
    def get_readout_single_channel(self, _channel_nr:int) -> float:
        """!
        Get analog value of a channel from the HAT adc or -1 when fails

        @param _channel_nr The channel nr wanted (starts at 0, so 0 is AI0)

        @return analog voltage or -1
        """
        if _channel_nr >= 0 and _channel_nr < 4:
            adc_code_array = bytearray(2)
            conf_data = 0x01 | 0x60 | (_channel_nr << 1)                          # single ended, single channel, only selected channel, the channel to be read (AIN3 = channel 4)

            self.__i2c_device.i2c_write_bytes(bytes([conf_data]))
            self.__i2c_device.read_from_into(adc_code_array)

            adc_raw_int = int(adc_code_array[1]  | adc_code_array[0] << 8)
            adc_code_int = adc_raw_int & 0x3ff
            voltage_float = float((self.__adc_ref_voltage / self.__adc_max_count) * adc_code_int)

            return voltage_float
        else:
            print("Channel " + str(_channel_nr) + " in ADC MAX11607 not available")
            return -1

    # --------------------------------------------------------------------------------------

    def get_readout_multiple_channels(self) -> []:
        """!
        Get analog values of the HAT adc. List has a size of 4. List pos 0 is channel AI0
        @return analog voltage in a list
        """

        adc_code_array = bytearray(8)

        conf_data = 0x01 | 0x06                                                 # single ended, multiple channel (0 un till last), last channel is AIN3 (channel 4)

        self.__i2c_device.i2c_write_bytes(bytes([conf_data]))
        self.__i2c_device.read_from_into(adc_code_array)

        for i in range(0, 4):
            adc_raw_int = int(adc_code_array[2 * i + 1]  | adc_code_array[2 * i] << 8)
            adc_code_int = adc_raw_int & 0x3ff
            voltage_float = float((self.__adc_ref_voltage / self.__adc_max_count) * adc_code_int)
            self.__adc_result_voltage[i] = voltage_float

        return self.__adc_result_voltage

    # --------------------------------------------------------------------------------------

