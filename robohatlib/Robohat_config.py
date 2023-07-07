#!/usr/bin/env python

try:
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
    from robohatlib.drivers.datastructs.McpInitStruct import McpInitStruct
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.constants.GPIO_Direction import GpioDirection
    from robohatlib.driver_ll.i2c.I2CBusDef import I2CBusDef
    from robohatlib.driver_ll.spi.SPI_Bus_Definition import SPI_Bus_Definition
    from robohatlib.driver_ll.definitions.GPODef import GPODef
    from robohatlib.driver_ll.definitions.MultiColorLedDef import MultiColorLedDef
    from robohatlib.hal.definitions.BuzzerDef import BuzzerDef
    from robohatlib.driver_ll.definitions.SerialDef import SerialDef
    from robohatlib.hal.definitions.IMUDef import IMUDef
    from robohatlib.driver_ll.definitions.IOExpanderDef import IOExpanderDef
except ImportError:
    raise ImportError("Failed to import needed dependencies for the Robohat_config")

ALARM_PERMITTED = False
ALARM_TIMEOUT_IN_SEC = 300
INIT_BEEP_PERMITTED = False

#-------------------settings of peripherals which are not user selectable

BUZZER_DEF = BuzzerDef("buzzer1", 18, 1000, 50)
SERIAL_DEF = SerialDef("debug_port", 1)

LEDRED_GPO_DEF = GPODef("led_red", 5)
LEDGREEN_GPO_DEF = GPODef("led_green", 6)
LEDBLUE_GPO_DEF = GPODef("led_blue", 26)
STATUSLED_DEF = MultiColorLedDef("statusled", LEDRED_GPO_DEF, LEDGREEN_GPO_DEF, LEDBLUE_GPO_DEF)


MINIMU9_LIS3MDL_I2C_DEF = I2CDeviceDef("IMU_1_I2C", 5, 0x1e)           # i2c bus5, address 0x1e
MINIMU9_LSM6DS33_I2C_DEF = I2CDeviceDef("IMU_2_I2C", 5, 0x6b)          # i2c bus5, address 0x6b
IMU_DEF = IMUDef("IMU", MINIMU9_LIS3MDL_I2C_DEF, MINIMU9_LSM6DS33_I2C_DEF)


HATADC_I2C_DEF = I2CDeviceDef("HATADC_I2C", 5, 0x34)                   # i2c bus5, address 0x34


POWERSHUTDOWN_GPO_DEF = GPODef("shutdown", 27)

#-------------------

SERVOASSEMBLY_1_I2C_BUS = 1
SERVOASSEMBLY_1_SPI_BUS = 0

SERVOASSEMBLY_2_I2C_BUS = 1
SERVOASSEMBLY_2_SPI_BUS = 0

SERVOASSEMBLY_COMMON_GPI = 4

#-------------------

IOEXPANDER_I2C_DEF = I2CDeviceDef("IOEXPANDER_I2C", 1, 0x20)          # i2c bus1, address 0x2
IOEXPANDER_INTERUPT_SETTINGS = [
    McpInitStruct(0, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(1, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(2, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(3, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(4, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(5, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(6, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(7, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    ]

IO_EXPANDER_DEF = IOExpanderDef("ioexpander", IOEXPANDER_I2C_DEF, 24, IOEXPANDER_INTERUPT_SETTINGS)


SERVOASSEMBLY_INTERUPT_SETTINGS = [
    McpInitStruct(0, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(1, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(2, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(3, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(4, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(5, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(6, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(7, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    ]


I2C1_DEF = I2CBusDef("main_i2c", 1, 3, 2, 100000)
I2C5_DEF = I2CBusDef("hat_adc", 5, 13, 12, 100000)
I2C6_DEF = I2CBusDef("unknown", 6, 23, 22, 100000)

SPI0_DEF = SPI_Bus_Definition("spi_bus_0", 0, 11, 10, 9)
SPI1_DEF = SPI_Bus_Definition("spi_bus_1", 1, 21, 20, 19)
SPI2_DEF = SPI_Bus_Definition("spi_bus_2", 2, 42, 41, 40)