try:
    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
except ImportError:
    print("Failed to import MAX11607")
    raise

class MAX11607:
    """
    ADC, 4 channel, 10 bit I2C
    """

    # --------------------------------------------------------------------------------------
    def __init__(self, _i2cdevice):
        #print("constructor MAX11607")
        self.__i2c_device = _i2cdevice

        self.__adc_max_count = 1024
        self.__adc_ref_voltage = 3.3
        self.__adc_result_voltage = [0.0] * 4  # allocates and fills alle elements of array with 0


    # --------------------------------------------------------------------------------------
    def init_adc(self):
        #print("init MAX11607")

        register_data = 0x80 | 0x2                                              # aak default, no reset
        conf_data = 0x01 | 0x06                                                 # single ended, multiple channel (0 untill last), last channel is AIN3 (channel 4)

        self.__i2c_device.i2c_write_bytes(bytes([register_data, conf_data]))

    # self.device.readinto(result)
    # --------------------------------------------------------------------------------------
    def get_voltage_readout_channel(self, _channel_nr:int) -> float:
        """!
        Get analog value of a channel from the HAT adc

        @param _channel_nr The channel nr wanted (starts at 1, so 1 is AI0)

        @return analog voltage
        """
        adc_code_array = bytearray(2)
        conf_data = 0x01 | 0x60 | (_channel_nr - 1 << 1)                          # single ended, single channel, only selected channel, the channel to be read (AIN3 = channel 4)

        self.__i2c_device.i2c_write_bytes(bytes([conf_data]))
        self.__i2c_device.read_from_into(adc_code_array)

        adcRawInt = (int) (adc_code_array[1]  | adc_code_array[0] << 8)
        adcCodeInt = adcRawInt & 0x3ff
        voltageFloat = float((self.__adc_ref_voltage / self.__adc_max_count) * adcCodeInt)

        return voltageFloat

    # --------------------------------------------------------------------------------------

    def get_readout_hatadc_mutiplechannels(self) -> []:
        """!
        Get analog values of the HAT adc

        @return analog voltage in a array
        """

        adccodearray = bytearray(8)

        confdata = 0x01 | 0x06                                                 # single ended, multiple channel (0 untill last), last channel is AIN3 (channel 4)

        self.__i2c_device.i2c_write_bytes(bytes([confdata]))
        self.__i2c_device.read_from_into(adccodearray)

        for i in range(0, 4):
            adcRawInt = (int) (adccodearray[2 * i + 1]  | adccodearray[2 * i] << 8)
            adcCodeInt = adcRawInt & 0x3ff
            voltageFloat = float((self.__adc_ref_voltage / self.__adc_max_count) * adcCodeInt)
            self.__adc_result_voltage[i] = voltageFloat

        return self.__adc_result_voltage

    # --------------------------------------------------------------------------------------