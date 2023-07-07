#!/usr/bin/env python

try:
    from robohatlib.drivers.MAX11137 import MAX11137
    from robohatlib.drivers.MAX11607 import MAX11607
except ImportError:
    print("Failed to import dependencies for the HatADC")
    raise


class HatADC:
    """!
    ADC onto the topboard.
    This ADC is also used fo accu-powermonitor
    """

    #---------------------------------------------------------------------
    def __init__(self, _iomanager, _hat_adc_i2c_def) -> None:
        """!
        @param _iomanager:
        @param _hat_adc_i2c_def:
        @return: None
        """

        i2c_device = _iomanager.get_i2c_device(_hat_adc_i2c_def)
        self.__hatadc = MAX11607(i2c_device)

    # init all adcs --------------------------------------------------------------------------------------
    def init_hatadc(self) -> None:
        """!
        Initializes the HAR Adc

        @return None
        """
        self.__hatadc.init_adc()

    # begin, hat adc functions --------------------------------------------------------------------------------------
    def get_voltage_readout_hatadc_channel(self, _channel_nr: int) -> float:
        """!
        Get analog value of a channel from the HAT adc

        @param _channel_nr The channel nr wanted (starts at 1, so 1 is AI0)

        @return analog voltage
        """
        return self.__hatadc.get_voltage_readout_channel(_channel_nr)

    def get_voltage_readout_hatadc_mutiplechannels(self) -> []:
        """!
        Get analog values of all channel from the HAT adc

        @return array of analog voltage
        """
        return self.__hatadc.get_readout_hatadc_mutiplechannels()
    # end, hat adc functions --------------------------------------------------------------------------------------

    def get_voltage_of_accu(self) -> float:
        """
        :return float:
        """
        return self.__hatadc.get_voltage_readout_channel(4)




