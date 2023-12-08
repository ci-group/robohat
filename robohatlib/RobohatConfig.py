"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Configuration for the Robohat lib. These settings aren't ment to be altered by the app programmer
do not alter
"""


try:
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef
    from robohatlib.drivers.datastructs.McpInitStruct import McpInitStruct
    from robohatlib.driver_ll.constants.InterruptTypes import InterruptTypes
    from robohatlib.driver_ll.constants.GpioDirection import GpioDirection
    from robohatlib.driver_ll.i2c.I2CBusDef import I2CBusDef
    from robohatlib.driver_ll.spi.SPIBusDef import SPIBusDef
    from robohatlib.driver_ll.definitions.GPODef import GPODef
    from robohatlib.driver_ll.definitions.LedDef import LedDef
    from robohatlib.driver_ll.definitions.MultiColorLedDef import MultiColorLedDef
    from robohatlib.hal.definitions.BuzzerDef import BuzzerDef
    from robohatlib.driver_ll.definitions.SerialDef import SerialDef
    from robohatlib.hal.definitions.IMUDef import IMUDef
    from robohatlib.driver_ll.definitions.IOExpanderDef import IOExpanderDef
except ImportError:
    raise ImportError("Failed to import needed dependencies for the RobohatConfig")


"""!
General settings
"""
DEBUG = False                                       # by changing this value to TRUE, more debug msg will be printed on the console
DEBUG_I2C = False


"""!
Alarm to user settings
"""
TIME_WINDOW_OF_SHORT_PROTECTION_POWER_GOOD_CHECK_SERVO_POWER = 1000     # time window in mS. When a DC/DC converter has a power-fail, which is longer than this time window, a message goes to the user
TIME_WINDOW_OF_SHORT_PROTECTION_RELEASE_SERVO_POWER = 500               # time in window, exit if no power-fault detected

ALARM_PERMITTED = True                              # sound an alarm when a system alert is present, such as to low accu capacity
ALARM_TIMEOUT_IN_SEC = 300                          # timeout between alarm
INIT_BEEP_PERMITTED = False                         # beep when started if True

"""!
Accu settings
"""
ACCU_INTERVAL_TIME_IN_SECONDS = 1                   # time between accu monitoring

ACCU_VOLTAGE_TO_LOW_THRESHOLD = 11.06               # threshold. below this value, the accu voltage is too low
ACCU_VOLTAGE_TO_HIGH_THRESHOLD = 13.00              # threshold, above this value, the accu voltage is too high
ACCU_WARNING_PERCENTAGE_2 = 20                      # threshold, warning to user at this point
ACCU_WARNING_PERCENTAGE_1 = 15                      # threshold, warning to user at this point
ACCU_VOLTAGE_ADC_FORMULA_A = 4.85533606358714       # parameter A of formula, form adc voltage to actual accu voltage (y = Ax + B)
ACCU_VOLTAGE_ADC_FORMULA_B = -0.512839675475041     # parameter B of formula, form adc voltage to actual accu voltage (y = Ax + B)
ACCU_LOG_DISPLAY_WHEN_TO_LOW = False                # keep on logging when accu voltage is too low
ACCU_LOG_DISPLAY_WHEN_TO_HIGH = False               # keep on logging when accu voltage is too high

# accu voltage to accu percentage LIST... depending on accu    voltage, percentage
ACCU_VOLTAGE_TO_PERCENTAGE_LIST =  [
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

POWER_SHUTDOWN_GPO_DEF = GPODef("shutdown", 27)                                 # definition of the shutdown GPIO pin, The pin which send the signal to the power monitor PCB

BUZZER_DEF = BuzzerDef("buzzer", 18, 1000, 50)                                  # definition for the buzzer, GPIO nr, initial frequency and initial duty cycle
SERIAL_DEF = SerialDef("debug_port", 1)                                         # definition for the serial port. not used?

LED_RED_GPO_DEF = LedDef("led_red", 5)                                          # definition of the RED LED (which is a part of the multicolor LED), the GPIO nr
LED_GREEN_GPO_DEF = LedDef("led_green", 6)                                      # definition of the GREEN LED (which is a part of the multicolor LED), the GPIO nr
LED_BLUE_GPO_DEF = LedDef("led_blue", 26)                                       # definition of the BLUE LED (which is a part of the multicolor LED), the GPIO nr
STATUS_LED_DEF = MultiColorLedDef("status_led",
                                  LED_RED_GPO_DEF,
                                  LED_GREEN_GPO_DEF,
                                  LED_BLUE_GPO_DEF)                             # definition of the multicolor LED

IMU_LIS3MDL_I2C_DEF = I2CDeviceDef("imu_lis3mdl", 5, 0x1e)                      # definition of a part of the IMU, the LLS3MDL part, i2c bus5, address 0x1e
IMU_LSM6DS33_I2C_DEF = I2CDeviceDef("imu_lsmds33", 5, 0x6b)                     # definition of a part of the IMU, the LSM6DS33 part, i2c bus5, address 0x6b
IMU_DEF = IMUDef("imu", IMU_LIS3MDL_I2C_DEF, IMU_LSM6DS33_I2C_DEF)              # definition of the IMU

TOPBOARD_ADC_I2C_DEF = I2CDeviceDef("topboard_adc", 5, 0x34)                    # definition of the TOPBOARD adc (is also used for power monitor) i2c bus5, address 0x34
TOPBOARD_IO_EXPANDER_I2C_DEF = I2CDeviceDef("topboard_io_expander", 1, 0x20)    # i2c bus1, i2c base address 0x20

TOPBOARD_IO_EXPANDER_INTERRUPT_SETTINGS = [
    McpInitStruct(0, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(1, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(2, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(3, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(4, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(5, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(6, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(7, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    ]                                                                           # interrupt settings of the IO expander, for each IO pin

TOPBOARD_INTERRUPT_GPI = 24                                                     # rpi-gpio pin which is the interrupt pin of the topboard
TOPBOARD_IO_EXPANDER_DEF = IOExpanderDef("topboard_io_expander",
                                         TOPBOARD_IO_EXPANDER_I2C_DEF,
                                         TOPBOARD_INTERRUPT_GPI,
                                         TOPBOARD_IO_EXPANDER_INTERRUPT_SETTINGS) # io expander definition of the topboard

# -------------------

SERVO_DEFAULT_PWM_FREQ = 50
"""!
Servo assembly board settings
"""
SERVOASSEMBLY_1_I2C_BUS = 1                                                         # I2C bus nr of servo assembly 1, connected by P3
SERVOASSEMBLY_1_SPI_BUS = 0                                                         # SPI bus nr of servo assembly 1, connected by P3

SERVOASSEMBLY_2_I2C_BUS = 1                                                         # I2C bus nr of servo assembly 2, connected by P4
SERVOASSEMBLY_2_SPI_BUS = 0                                                         # SPI bus nr of servo assembly 2, connected by P4

SERVOASSEMBLY_INTERRUPT_GPI = 4
SERVOASSEMBLY_I2C_DEF = I2CDeviceDef("io_expander", 1, 0x20)                        # i2c bus1, i2c base address 0x20

SERVOASSEMBLY_INTERRUPT_SETTINGS = [
    McpInitStruct(0, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(1, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(2, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    McpInitStruct(3, GpioDirection.GPIO_INPUT, InterruptTypes.INT_RISING),
    ]                                                                               # interrupt settings of the IO expander, for each IO pin

SERVOASSEMBLY_EXPANDER_DEF = IOExpanderDef("power_monitor_expander",
                                           SERVOASSEMBLY_I2C_DEF,
                                           SERVOASSEMBLY_INTERRUPT_GPI,
                                           SERVOASSEMBLY_INTERRUPT_SETTINGS)        # io expander definition of an assembly board

"""!
I2C bus definitions 
"""
I2C1_DEF = I2CBusDef("main_i2c", 1, 3, 2, 100000)                                   # definition for i2c-bus 1: name, bus-nr, scl-io, sda-io, freq
I2C5_DEF = I2CBusDef("hat_adc", 5, 13, 12, 100000)                                  # definition for i2c-bus 5: name, bus-nr, scl-io, sda-io, freq
I2C6_DEF = I2CBusDef("unknown", 6, 23, 22, 100000)                                  # definition for i2c-bus 6: name, bus-nr, scl-io, sda-io, freq

"""!
SPI bus definitions
"""
SPI0_DEF = SPIBusDef("spi_bus_0", 0, 11, 10, 9)                                     # definition for spi-bus 0: name, bus-nr, clk, mosi, miso
SPI1_DEF = SPIBusDef("spi_bus_1", 1, 21, 20, 19)                                    # definition for spi-bus 2: name, bus-nr, clk, mosi, miso
SPI2_DEF = SPIBusDef("spi_bus_2", 2, 42, 41, 40)                                    # definition for spi-bus 2: name, bus-nr, clk, mosi, miso

POWER_SHUTDOWN_PIN_IO_TOPBOARD = 0

DEFAULT_SERVO_UPDATE_VALUE = 1
DEFAULT_DELAY_BETWEEN_ACTION = 0.001
INITIAL_POS_OF_SERVOS = 90.0