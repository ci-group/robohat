from robohatlib.hal.assemblyboard.servo.ServoBoard import ServoBoard
from robohatlib.hal.assemblyboard.PowerMonitorAndIO import POWERMONITORANDIO
from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef

from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
from robohatlib.driver_ll.spi.SPIDeviceDef import SPIDeviceDef


BASE_ADDRESS_MCP23008 = 0x20
BASE_ADDRESS_PCA9685 = 0x40

class ServoAssembly:

    def __init__(self, _iomanager, _servo_config, _i2c_bus_nr, _spi_bus_nr, _mcp_interrupt_definition = None):

        self.__servo_config = _servo_config

        #----------------------------
        i2c_def_pwm = I2CDeviceDef(_servo_config.get_name(), _i2c_bus_nr, BASE_ADDRESS_PCA9685, _servo_config.get_sw1_pwm_address())
        i2c_device_pwm = _iomanager.get_i2c_device(i2c_def_pwm)

        spi_def_adc = SPIDeviceDef(_servo_config.get_name(), _spi_bus_nr, _servo_config.get_cs_adc_angle_readout())
        spi_device_adc = _iomanager.get_spi_device(spi_def_adc)

        if i2c_device_pwm is not None and spi_device_adc is not None:
            self.__servo_board = ServoBoard(i2c_device_pwm, spi_device_adc)
        else:
            self.__servo_board = None
        # ----------------------------

        # ----------------------------
        gpi_interrupt_definition = GPIInterruptDef.from_mcp23008_interrupt_definition(_mcp_interrupt_definition)
        _iomanager.register_interrupt(gpi_interrupt_definition)

        i2c_def_power_monitor = I2CDeviceDef(_servo_config.get_name() + "_I2C", _i2c_bus_nr, BASE_ADDRESS_MCP23008, _servo_config.get_sw2_power_good_address())
        i2c_device_power_monitor = _iomanager.get_i2c_device(i2c_def_power_monitor)

        if i2c_device_power_monitor is not None:
            self.__power_monitor_and_io = POWERMONITORANDIO(i2c_device_power_monitor, _mcp_interrupt_definition)
        else:
            self.__power_monitor_and_io = None
        # ----------------------------


    def init_servo_assembly(self, _servo_datas_array: []):
        """
        Initializes servo assembly

        @param _servo_datas_array:
        :return:
        """
        if  self.__servo_board is not None:
            self.__servo_board.init_servo_board(_servo_datas_array)

    #--------------------------------------------------------------------------------------

    def set_servo_angle(self, _servo_nr: int, _wanted_angle: float) -> None:
        """!
        Set the angle servo in degree

        @param _servo_nr The servo nr wanted (starts at 1)
        @param _wanted_angle wanted angle

        @return angle of connected servo in degree
        """
        if self.__servo_board is not None:
            self.__servo_board.set_servo_angle(_servo_nr, _wanted_angle)

    def get_servo_angle(self, _servo_nr: int) -> float:
        """!
        Get angle of connected servo in degree

        @param _servo_nr The servo nr wanted (starts at 1)
        @return angle of connected servo in degree, or 0 when not available
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_angle(_servo_nr)
        return 0

    # --------------------------------------------------------------------------------------

    def set_all_servos_angle(self, _wanted_angles) -> None:
        """!
        Set the angle of connected servos in degree

        @param _wanted_angles array of the angles

        @return angle of connected servo in degree
        """
        self.__servo_board.set_all_servos_angle(_wanted_angles)

    def get_all_servos_angle(self) -> []:
        """!
        @return angles of servos in degree
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_all_servos_angle()
        return []

    # --------------------------------------------------------------------------------------

    def get_servo_adc_readout_single_channel(self, _servo_nr: int) -> float:
        """!
        Get voltage of the potentiometer of the connected servo in vol

        @param _servo_nr The servo nr wanted (starts at 1)
        @return voltage of connected servo in volt or 0 when not available
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_readout_adc_single_channel(_servo_nr)
        return 0

    def get_adc_readout_multiple_channels(self) -> []:
        """!
        @return voltages of the potentiometer of all the servos in volt
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_readout_adc_multiple_channels()
        return []

    # --------------------------------------------------------------------------------------
    def get_servo_is_connected(self, _servo_nr: int) -> bool:
        """!
        Checks if servo is connected. Returns False when not connected

        @param _servo_nr The servo nr
        @return: Returns False when not connected
        """
        if self.__servo_board is not None:
            return self.__servo_board.get_servo_is_connected(_servo_nr)
        return False

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        return self.__servo_config.get_name()
    # --------------------------------------------------------------------------------------

    def get_sw1_pwm_address(self) -> int:
        return  self.__servo_config.get_sw1_pwm_address()

    # --------------------------------------------------------------------------------------

    def get_sw2_power_good_address(self) -> int:
        return self.__servo_config.get_sw2_power_good_address()

    # --------------------------------------------------------------------------------------

    def get_cs_adc_angle_readout(self) -> int:
        return self.__servo_config.get_cs_adc_angle_readout()

    # --------------------------------------------------------------------------------------

