#!/usr/bin/env python

try:
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
    from robohatlib.drivers.datastructs.McpInitStruct import McpInitStruct
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.constants.GPIO_Direction import GpioDirection
    from robohatlib.driver_ll.i2c.I2CBusDef import I2CBusDef
    from robohatlib.driver_ll.spi.SPIBusDef import SPIBusDef
    from robohatlib.driver_ll.definitions.GPODef import GPODef
    from robohatlib.driver_ll.definitions.MultiColorLedDef import MultiColorLedDef
    from robohatlib.hal.definitions.BuzzerDef import BuzzerDef
    from robohatlib.driver_ll.definitions.SerialDef import SerialDef
    from robohatlib.hal.definitions.IMUDef import IMUDef
    from robohatlib.driver_ll.definitions.IOExpanderDef import IOExpanderDef
except ImportError:
    raise ImportError("Failed to import needed dependencies for the Robohat_config")

"""!
Configuration for the Robohat lib. These settings aren't ment to be altered by the app programmer
do not alter
"""

"""!
Some system settings
"""
ALARM_PERMITTED = False                             # sound an alarm when a system alert is present, such as to low accu capacity
ALARM_TIMEOUT_IN_SEC = 300                          # timeout between alarm
INIT_BEEP_PERMITTED = False                         # beep when started

ACCU_INTERVAL_TIME_IN_SECONDS = 1
ACCU_VOLTAGE_WHEN_FULL = 12.6
ACCU_VOLTAGE_TO_LOW_THRESHOLD = 11.06
ACCU_VOLTAGE_ADC_MULTIPLIER = 4.3                   # aangepast 4-7-23, was 8.0
ACCU_LOG_DISPLAY_WHEN_TO_LOW = False

# Voltage to percentage array... depending on accu used
ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY =  [
                                    [9.6,	0],
                                    [9.82,	1],
                                    [10.83,	5],
                                    [11.06,	10],
                                    [11.12,	15],
                                    [11.18,	20],
                                    [11.24,	25],
                                    [11.3,	30],
                                    [11.36,	35],
                                    [11.39,	40],
                                    [11.45,	45],
                                    [11.51,	50],
                                    [11.56,	55],
                                    [11.62,	60],
                                    [11.74,	65],
                                    [11.86,	70],
                                    [11.95,	75],
                                    [12.07,	80],
                                    [12.25,	85],
                                    [12.33,	90],
                                    [12.5, 95],
                                    [12.6, 100]
                                    ]

"""!
Device settings
"""
BUZZER_DEF = BuzzerDef("buzzer", 18, 1000, 50)      # definition for the buzzer, GPIO nr, initial frequency and initial duty cycle
SERIAL_DEF = SerialDef("debug_port", 1)             # definition for the serial port. (todo) AT THIS MOMENT NOT IMPLEMENTED

LEDRED_GPO_DEF = GPODef("led_red", 5)               # definition of the multicolor LED, the RED part, GPIO nr
LEDGREEN_GPO_DEF = GPODef("led_green", 6)           # definition of the multicolor LED, the GREEN part, GPIO nr
LEDBLUE_GPO_DEF = GPODef("led_blue", 26)            # definition of the multicolor LED, the BLUE part, GPIO nr
STATUSLED_DEF = MultiColorLedDef("statusled", LEDRED_GPO_DEF, LEDGREEN_GPO_DEF, LEDBLUE_GPO_DEF)    # definition of the multicolor LED

MINIMU9_LIS3MDL_I2C_DEF = I2CDeviceDef("IMU_1_I2C", 5, 0x1e)                    # definition of the IMU, LLS3MDL part, i2c bus5, address 0x1e
MINIMU9_LSM6DS33_I2C_DEF = I2CDeviceDef("IMU_2_I2C", 5, 0x6b)                   # definition of the IMU, LSM6DS33 part, i2c bus5, address 0x6b
IMU_DEF = IMUDef("IMU", MINIMU9_LIS3MDL_I2C_DEF, MINIMU9_LSM6DS33_I2C_DEF)      # definition of the IMU

HATADC_I2C_DEF = I2CDeviceDef("hatadc_i2c", 5, 0x34)                            # definition of the TOPBOARD adc (is also used for power monitor) i2c bus5, address 0x34

POWERSHUTDOWN_GPO_DEF = GPODef("shutdown", 27)                                  # definition of the shutdown GPIO pin

IOEXPANDER_I2C_DEF = I2CDeviceDef("ioexpander_i2c", 1, 0x20)          # i2c bus1, address 0x2
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

# -------------------
"""!
Servo assembly board settings
"""
SERVOASSEMBLY_1_I2C_BUS = 1
SERVOASSEMBLY_1_SPI_BUS = 0

SERVOASSEMBLY_2_I2C_BUS = 1
SERVOASSEMBLY_2_SPI_BUS = 0

SERVOASSEMBLY_COMMON_GPI = 4

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

"""!
I2C definitions
"""
I2C1_DEF = I2CBusDef("main_i2c", 1, 3, 2, 100000)       # bus 1, scl, sda, freq
I2C5_DEF = I2CBusDef("hat_adc", 5, 13, 12, 100000)      # bus 5, scl, sda, freq
I2C6_DEF = I2CBusDef("unknown", 6, 23, 22, 100000)      # bus 6, scl, sda, freq

"""!
SPI definitions
"""
SPI0_DEF = SPIBusDef("spi_bus_0", 0, 11, 10, 9)         # bus 0, name, bus, clk, mosi, miso
SPI1_DEF = SPIBusDef("spi_bus_1", 1, 21, 20, 19)        # bus 1, name, bus, clk, mosi, miso
SPI2_DEF = SPIBusDef("spi_bus_2", 2, 42, 41, 40)        # bus 2, name, bus, clk, mosi, miso
