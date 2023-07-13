#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

try:
    import spidev
except ImportError:
    raise ImportError("spidev not found.")

try:
    from robohatlib.driver_ll.spi.SPI_Device import SPI_Device
except ImportError:
    raise ImportError("failed to resolve all dependencies for MAX11137")

#--------------------------------------------------------------------------------------
#RETURN
#--------------------------------------------------------------------------------------

CHANNEL_MSB  = 0
DATA_MSB = 4

#--------------------------------------------------------------------------------------
#CONF
#--------------------------------------------------------------------------------------
ADC_CONFIGURATION_BASE   = 0b1000000000000000
REFSEL_LSB = 10
AVG_LSB  =  9
NAVG_LSB = 7
NSCAN_LSB = 5
SPM_LSB = 3
ECHO_LSB = 2

REFSEL_EXTERNAL_SINGLEENDED = 0b0
AVG_OFF = 0b0
AVG_ON = 0b1
NAVG_1_CONV = 0b000
NSCAN_RETURN_4 = 0b00
NSCAN_RETURN_8 = 0b01
NSCAN_RETURN_16 = 0b10
NSCAN_RETURN_32 = 0b11
SPM_NORMAL = 0b11
ECHO_OFF = 0b0

#--------------------------------------------------------------------------------------
ADC_RANGE_BASE = 0b1001100000000000
VREF_LSB = 3

VREF_HALF = 0b00000000
VREF_FULL = 0b11111111

#--------------------------------------------------------------------------------------
ADC_UNIPOLAIR_BASE = 0b1000100000000000    # not used
ADC_BIPOLAR_BASE = 0b1001000000000000    # not used

ADC_CUSTOMSCAN0_BASE = 0b1010000000000000
ADC_CUSTOMSCAN1_BASE = 0b1010100000000000
ADC_CUSTOMSCAN_LSB = 3
ADC_CUSTOMSCAN_ALL = 0b11111111

ADC_SAMPLESET_BASE = 0b1011000000000000    # not used

#--------------------------------------------------------------------------------------
ADC_MODE_CONTROL_BASE = 0b0000000000000000

SCAN_LSB    = 11
CHSEL_LSB   =  7
RESET_LSB   =  5
PM_LSB      =  3
CHAN_ID_LSB =  2
SWCNV_LSB   =  1

SCAN_BITS_NA = 0b0000
SCAN_BITS_STANDARD_INT = 0b0011
SCAN_BITS_UPPER_INT = 0b0101
SCAN_BITS_CUSTOM_INT = 0b0111
SCAN_BITS_MANUAL = 0b0001
SCAN_BITS_SAMPLESET = 0b1001

CHSEL_BITS_AIN0 = 0b0000
CHSEL_BITS_AIN1 = 0b0001
CHSEL_BITS_AIN2 = 0b0010

RESET_BITS_NORESET = 0b00
PM_BITS_NORMAL = 0b00
CHAN_ID_BITS = 0b1
SWCNV_BITS = 0b1



#--------------------------------------------------------------------------------------

class MAX11137:
    # variables
    __adcrefvoltage = 3.0               # reference voltage for the ADC
    __adcmaxcount = 4095                # max count, (12 bit = 4095

    __debug = False

    __adcresultvoltage = [0.0] * 16         # allocates and fills alle elements of array with 0

    # --------------------------------------------------------------------------------------
    def __init__(self, _spi_device:SPI_Device):
        #print("Constructor MAX11137")
        self.__spi_device = _spi_device

    # --------------------------------------------------------------------------------------
    '''!
    public method, init the adc
    '''
    def init_adc(self):
        #print("init MAX11137")


        # spiADC.read0 = False                           # Read 0 bytes after transfer to lower CS if cshigh == True, bestaat niet rpi
        # spiADC.bits_per_word(16)                       # seems not to be supported at RPi

        adc_configuration = ADC_CONFIGURATION_BASE
        adc_configuration = self.__updateRegisterValue(adc_configuration, REFSEL_LSB, REFSEL_EXTERNAL_SINGLEENDED)
        adc_configuration = self.__updateRegisterValue(adc_configuration, AVG_LSB, AVG_ON)
        adc_configuration = self.__updateRegisterValue(adc_configuration, NAVG_LSB, NSCAN_RETURN_32)
        adc_configuration = self.__updateRegisterValue(adc_configuration, NSCAN_LSB, NSCAN_RETURN_16)
        adc_configuration = self.__updateRegisterValue(adc_configuration, SPM_LSB, SPM_NORMAL)
        adc_configuration = self.__updateRegisterValue(adc_configuration, ECHO_LSB, ECHO_OFF)
        self.__spi_device.writeRegister(adc_configuration)

        adc_range = ADC_RANGE_BASE
        adc_range = self.__updateRegisterValue(adc_range, VREF_LSB, VREF_FULL)
        self.__spi_device.writeRegister(adc_range)

        adc_custom_scan0 = ADC_CUSTOMSCAN0_BASE
        adc_custom_scan0 = self.__updateRegisterValue(adc_custom_scan0, ADC_CUSTOMSCAN_LSB, ADC_CUSTOMSCAN_ALL)
        self.__spi_device.writeRegister(adc_custom_scan0)

        adc_custom_scan1 = ADC_CUSTOMSCAN1_BASE
        adc_custom_scan1 = self.__updateRegisterValue(adc_custom_scan1, ADC_CUSTOMSCAN_LSB, ADC_CUSTOMSCAN_ALL)
        self.__spi_device.writeRegister(adc_custom_scan1)

    # --------------------------------------------------------------------------------------
    '''!
    public method, resets the adc
    '''
    def reset_adc(self):
        self.__spi_device.writeRegister(0x0040)

    # --------------------------------------------------------------------------------------
    '''!
    public method, get voltage of 1 channel of the ADC, returns a double
    '''
    def get_readout_adc_servo_nr(self, _servo_nr: int) -> float:
        """!
        Get voltage of the potentiometer of the connected servo in vol

        @param _servo_nr The servo nr wanted (starts at 0)

        @return voltage of the potentiometer of the connected servo in volt
        """
        if _servo_nr >= 0 and _servo_nr < 16:
            # adc_mode_control = 0b0000000000000000
            # adc_mode_control = self.__updateRegisterValue(adc_mode_control, SCAN_LSB, SCAN_BITS_MANUAL)
            # adc_mode_control = self.__updateRegisterValue(adc_mode_control, CHSEL_LSB, _servo_nr)
            # adc_mode_control = self.__updateRegisterValue(adc_mode_control, RESET_LSB, RESET_BITS_NORESET)
            # adc_mode_control = self.__updateRegisterValue(adc_mode_control, PM_LSB, PM_BITS_NORMAL)
            # adc_mode_control = self.__updateRegisterValue(adc_mode_control, CHAN_ID_LSB, CHAN_ID_BITS)
            # adc_mode_control = self.__updateRegisterValue(adc_mode_control, SWCNV_LSB, SWCNV_BITS)
            # value = self.__give_result_adc(adc_mode_control)

            #4-7-23
            # instead of using the channel auto increment, just read the whole array... was a bug
            value_array = self.get_readout_adc_mutiplechannels()
            return value_array[_servo_nr]
        else:
            print("Servo range not valid")
            return -1

    # --------------------------------------------------------------------------------------
    '''!
    public method, get voltage of all 16 channels of the ADC. returns an array
    '''
    def  get_readout_adc_mutiplechannels(self) -> []:
        """!
        @return voltages of the potentiometer of all the servos in volt
        """

        adc_mode_control = 0b0000000000000000
        adc_mode_control = self.__updateRegisterValue(adc_mode_control, SCAN_LSB, SCAN_BITS_STANDARD_INT)
        adc_mode_control = self.__updateRegisterValue(adc_mode_control, CHSEL_LSB, 15)
        adc_mode_control = self.__updateRegisterValue(adc_mode_control, RESET_LSB, RESET_BITS_NORESET)
        adc_mode_control = self.__updateRegisterValue(adc_mode_control, PM_LSB, PM_BITS_NORMAL)
        adc_mode_control = self.__updateRegisterValue(adc_mode_control, CHAN_ID_LSB, CHAN_ID_BITS)
        adc_mode_control = self.__updateRegisterValue(adc_mode_control, SWCNV_LSB, SWCNV_BITS)

        count_adc = self.__spi_device.writeRegister(adc_mode_control)
        value_raw_int = int(count_adc & 0x0fff)
        channel_raw_int = int(count_adc >> 12)
        voltage_float = float((self.__adcrefvoltage / self.__adcmaxcount) * value_raw_int)
        self.__adcresultvoltage[channel_raw_int] = voltage_float

        for  i  in range(0,16):
            adc_mode_control = 0b0000000000000000
            adc_mode_control = self.__updateRegisterValue(adc_mode_control, SCAN_BITS_NA, SCAN_BITS_NA)

            count_adc = self.__spi_device.writeRegister(adc_mode_control)
            value_raw_int = int(count_adc & 0x0fff)
            channel_raw_int = int(count_adc >> 12)
            voltage_float = float((self.__adcrefvoltage / self.__adcmaxcount) * value_raw_int)
            self.__adcresultvoltage[channel_raw_int] = voltage_float

        return self.__adcresultvoltage

    # --------------------------------------------------------------------------------------

    '''!
    private method, to get the result out of the ADC in voltage 
    '''
    def __give_result_adc(self, _adc_mode_control) -> float:
        count_adc = self.__spi_device.writeRegister(_adc_mode_control)
        value_raw_int = int(count_adc & 0x0fff)
        channel_raw_int = int(count_adc >> 12)
        voltage_float = float((self.__adcrefvoltage / self.__adcmaxcount) * value_raw_int)

        if self.__debug is True:
            print("-->" + str(self.__spi_device.get_spi_bus_nr()) + " " + hex(count_adc) + " bin: " + bin(count_adc)[2:].zfill(16) + " channel: " + str(channel_raw_int) + " code: " + str(value_raw_int) + " voltage: " + str(voltage_float) + " V")

        return voltage_float


    # --------------------------------------------------------------------------------------


    '''!
    private method, to alter a value swith bitvalue and a bit position
    '''
    def __updateRegisterValue(self, previous_value, bit_pos, bit_value):
        return_value = previous_value | (bit_value << bit_pos)
        return return_value

    # --------------------------------------------------------------------------------------


