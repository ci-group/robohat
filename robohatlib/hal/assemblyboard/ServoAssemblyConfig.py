


class ServoAssemblyConfig:
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __init__(self, _name:str, _sw1_pwm_address:int, _sw2_power_good_address:int, _cs_adc_angle_readout:int):
        #print("Constuctor of ServoBoardConfig")
        self.__name = _name
        self.__sw1_pwm_address = _sw1_pwm_address
        self.__sw2_power_good_address = _sw2_power_good_address
        self.__cs_adc_angle_readout = _cs_adc_angle_readout

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_sw1_pwm_address(self) -> int:
        return  self.__sw1_pwm_address

    # --------------------------------------------------------------------------------------

    def get_sw2_power_good_address(self) -> int:
        return self.__sw2_power_good_address

    # --------------------------------------------------------------------------------------

    def get_cs_adc_angle_readout(self) -> int:
        return self.__cs_adc_angle_readout

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------