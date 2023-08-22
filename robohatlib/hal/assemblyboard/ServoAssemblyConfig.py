"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.hal.assemblyboard.PwmPlug import PwmPlug
except ImportError:
    print("Failed to import all dependencies for ServoAssemblyConfig")
    raise


class ServoAssemblyConfig:
    """!
    This configuration class is needed to get the hardware working. There can multiple assemblies connected at the RPi
    """

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __init__(self, _name:str, _sw1_pwm_address:int, _sw2_power_good_address:int, _cs_adc_angle_readout:PwmPlug):
        """!
        Constructor of this definition
        @param _name: name of the assembly
        @param _sw1_pwm_address:  sw1 value
        @param _sw2_power_good_address: sw2 value
        @param _cs_adc_angle_readout: spi cs value
        """

        self.__name = _name
        self.__sw1_pwm_address = _sw1_pwm_address
        self.__sw2_power_good_address = _sw2_power_good_address
        self.__cs_adc_angle_readout = _cs_adc_angle_readout

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Gives the name of this definition
        @return: name
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_sw1_pwm_address(self) -> int:
        """!
        Value of sw1 on the Servo PCB
        @return: sw1 value
        """

        return self.__sw1_pwm_address
    # --------------------------------------------------------------------------------------

    def get_sw2_power_good_address(self) -> int:
        """!
        Value of sw2 on the Servo PCB
        @return: sw2 value
        """
        return self.__sw2_power_good_address

    # --------------------------------------------------------------------------------------

    def get_cs_adc_angle_readout(self) -> PwmPlug:
        """!
        Value of cs of SPI of the Servo PCB, determined by the flat-cable
        @return: cs
        """
        return self.__cs_adc_angle_readout

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------