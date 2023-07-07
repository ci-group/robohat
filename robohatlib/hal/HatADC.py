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
        if i2c_device is not None:
            self.__hat_adc = MAX11607(i2c_device)
        self.__hat_adc = None

    # init all adcs --------------------------------------------------------------------------------------
    def init_hat_adc(self) -> None:
        """!
        Initializes the HAT Adc

        @return None
        """

        if self.__hat_adc is not None:
            self.__hat_adc.init_adc()

    # begin, hat adc functions --------------------------------------------------------------------------------------
    def get_voltage_readout_hat_adc_channel(self, _channel_nr: int) -> float:
        """!
        Get analog value of a channel from the HAT adc

        @param _channel_nr The channel nr wanted (starts at 1, so 1 is AI0)

        @return analog voltage, or 0.0 when not available
        """
        if self.__hat_adc is not None:
            return self.__hat_adc.get_voltage_readout_channel(_channel_nr)
        return 0.0

    def get_voltage_readout_hatadc_mutiplechannels(self) -> []:
        """!
        Get analog values of all channel from the HAT adc

        @return array of analog voltage or None when not available
        """
        if self.__hat_adc is not None:
            return self.__hat_adc.get_readout_hatadc_mutiplechannels()
        return []

    # end, hat adc functions --------------------------------------------------------------------------------------

    def get_voltage_of_accu(self) -> float:
        """!
        Get voltage on pin4, which the accu is connected to
        @return float: voltage of accu or 0.0 when not available
        """

        if self.__hat_adc is not None:
            return self.__hat_adc.get_voltage_readout_channel(4)
        return 0.0



