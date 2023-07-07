try:
    import time, threading
    import statistics
    import subprocess
    from robohatlib import Robohat_config
    from time import sleep
except ImportError:
    print("Failed to import needed dependencies for the Robohat class")
    raise


WAIT_SECONDS = 1
SIZE_OF_WINDOW = 5

VOLTAGE_FULL_BATTERY = 12.6
ACCU_VOLTAGE_MULTIPLIER = 8 #4.3 # aangepast 4-7-23   8.0
ACCU_EMPTY_THRESHOLD = 11.06

BATTERY_ARRAY = [
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

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class PowerManagement:

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __init__(self, _iomanager, _adc_hat, _powershutdown_gpo_def):
        self.__adc_hat = _adc_hat
        self.__shutdown_gpo = _iomanager.get_gpo(_powershutdown_gpo_def)

        self.__timerIsRunning = False
        self.__accu_percentage_capacity = 0
        self.__accu_voltage = 0
        self.__accu_capacity_ok = False
        self.__raw_accu_voltages_array = [12.6] * SIZE_OF_WINDOW

        self.__signaling_device = None
        self.__shutdown_in_progress = False
        self.__counter_prevent_startup_power_fail = 0

        self.__battery_check_started = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def init_power_management(self) -> None:
        """
        Initializes power management

        @return None
        """
        print("init_powerMgt")
        self.__timerIsRunning = True
        self.__start_timer_power_management()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __start_timer_power_management(self) -> None:
        timer = threading.Timer(WAIT_SECONDS, self.timer_callback)
        if self.__timerIsRunning is True:
            timer.start()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def stop_timer_power_management(self) -> None:
        self.__timerIsRunning = False
    # --------------------------------------------------------------------------------------
    def timer_callback(self) -> None:
        adc_accu_voltage = self.__adc_hat.get_voltage_of_accu()
        calculated_accu_voltage = adc_accu_voltage * ACCU_VOLTAGE_MULTIPLIER
        self.__insert_power_voltage(calculated_accu_voltage)
        self.__start_timer_power_management()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def is_timer_running(self) -> bool:
        return self.__timerIsRunning

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_accu_percentage_capacity(self) -> int:
        return self.__accu_percentage_capacity

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_accu_voltage(self) -> float:
        return self.__accu_voltage

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def is_accu_capacity_ok(self) -> bool:
        return self.__accu_capacity_ok

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __insert_power_voltage(self, _raw_accu_voltage):

        #shift new value in array
        for index in range(1, SIZE_OF_WINDOW, 1):
            self.__raw_accu_voltages_array[index - 1] = self.__raw_accu_voltages_array[index]

        self.__raw_accu_voltages_array[SIZE_OF_WINDOW - 1] = _raw_accu_voltage

        self.__counter_prevent_startup_power_fail += 1
        if self.__counter_prevent_startup_power_fail < SIZE_OF_WINDOW:
            return

        self.__counter_prevent_startup_power_fail = SIZE_OF_WINDOW    # prevent overrun

        self.__accu_voltage = statistics.median(map(float, self.__raw_accu_voltages_array)) # create median

        if self.__accu_voltage > 0.5:
            self.__accu_percentage_capacity = self.__calculate_percentage_from_voltage(self.__accu_voltage)
            if self.__accu_voltage < ACCU_EMPTY_THRESHOLD:
                self.__accu_capacity_ok = False

                if self.__signaling_device is not None:
                    self.__signaling_device.signal_system_alarm()
                print("accu capacity to low, only {0:3.2f} %".format(self.__accu_percentage_capacity))

            elif self.__accu_capacity_ok is False and self.__accu_voltage > ACCU_EMPTY_THRESHOLD + (ACCU_EMPTY_THRESHOLD * 0.02):
                self.__accu_capacity_ok = True

        else:
            self.__accu_percentage_capacity = -1
            print("no detection of accu capacity")

        if self.__battery_check_started is False:
            self.__battery_check_started = True

            print("accu monitor active")
            print("accu voltage: {0:2.2f} V".format(self.__accu_voltage))
            print("accu percentage: {0:3.2f} %".format(self.__accu_percentage_capacity))
            print("accu is OK: " + str(self.__accu_capacity_ok))

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # gets percentage out of list, and interpolates the voltages between the elements of the list
    def __calculate_percentage_from_voltage(self, _accu_voltage) -> float:

        if _accu_voltage <= BATTERY_ARRAY[0] [0]:
            return 0

        if _accu_voltage >= BATTERY_ARRAY[len(BATTERY_ARRAY) - 1] [0]:
            return 100

        for index in range(0, len(BATTERY_ARRAY) - 1, 1):
            voltage_low = BATTERY_ARRAY[index] [0]
            voltage_high = BATTERY_ARRAY[index + 1] [0]

            diff_voltage = voltage_high - voltage_low
            diff_perc = BATTERY_ARRAY[index + 1] [1] - BATTERY_ARRAY[index] [1]
            perc_per_volt = diff_perc / diff_voltage

            if voltage_low <= _accu_voltage <= voltage_high:
                remainder_volt = voltage_high - _accu_voltage
                remainder_perc = remainder_volt * perc_per_volt

                percentage = BATTERY_ARRAY[index] [1] + remainder_perc
                return percentage

        self.shutdown()

        return 100

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def add_signaling_device(self, _signaling_device):
        self.__signaling_device = _signaling_device

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------


    def shutdown(self):
        if self.__shutdown_in_progress is True:
            return

        print("Power shutdown in 1 minute")

        self.__shutdown_gpo.set_high()
        sleep(1)
        self.__shutdown_gpo.set_low()

        if self.__signaling_device is not None:
            self.__signaling_device.signal_system_alarm()

        self.__shutdown_in_progress = True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
