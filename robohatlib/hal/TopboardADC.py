"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.drivers.MAX11137 import MAX11137
    from robohatlib.drivers.MAX11607 import MAX11607
except ImportError:
    print("Failed to import dependencies for the HatADC")
    raise

CHANNEL_ACCU_VOLTAGE = 3

class TopboardADC:
    """!
    ADC onto the topboard.
    This ADC is also used fo accu-power-monitor
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
        else:
            self.__hat_adc = None

    # init all adcs --------------------------------------------------------------------------------------
    def init_topboard_adc(self) -> None:
        """!
        Initializes the HAT Adc

        @return None
        """

        if self.__hat_adc is not None:
            self.__hat_adc.init_adc()

    # --------------------------------------------------------------------------------------
    def exit_program(self) -> None:
        """
        Cleans up, when user want to shut down
        @return: None
        """


    # begin, hat adc functions --------------------------------------------------------------------------------------
    def get_adc_single_channel(self, _channel_nr: int) -> float:
        """!
        Get analog value of a channel from the HAT adc

        @param _channel_nr The channel nr wanted (starts at 1, so 1 is AI0)

        @return analog voltage, or -1 when not available
        """

        if self.__hat_adc is not None:
            if _channel_nr >= 0 and _channel_nr < 4:
                return self.__hat_adc.get_readout_single_channel(_channel_nr)
            else:
                print("Unknown channel nr")
        else:
            print ("hat adc not found ??")
        return -1

    def get_adc_multiple_channels(self) -> []:
        """!
        Get analog values of all channel from the HAT adc

        @return a list of analog voltage or None when not available
        """
        if self.__hat_adc is not None:
            return self.__hat_adc.get_readout_multiple_channels()
        return []

    # end, hat adc functions --------------------------------------------------------------------------------------

    def get_voltage_of_battery(self) -> float:
        """!
        Get voltage on pin4, which the accu is connected to
        @return float: voltage of accu or 0.0 when not available
        """

        if self.__hat_adc is not None:
            return self.__hat_adc.get_readout_single_channel(CHANNEL_ACCU_VOLTAGE)
        return 0.0

