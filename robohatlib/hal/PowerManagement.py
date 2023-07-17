try:
    import time
    import threading
    import statistics
    import subprocess
    import os
    from time import sleep
    from robohatlib import Robohat_config
    from robohatlib.driver_ll.definitions.GPODef import GPODef
    from robohatlib.hal.HatADC import HatADC
    from robohatlib.driver_ll.IOHandler import IOHandler


except ImportError:
    print("Failed to import needed dependencies for the Robohat class")
    raise


ACCU_CHECK_SIZE_OF_WINDOW = 5

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


class PowerManagement:
    """!
    Class to measure the accu capacity
    """

    def __init__(self, _io_handler: IOHandler, _adc_hat: HatADC, _shutdown_gpo_def: GPODef):
        """!
        @param _io_handler: the IO handler
        @param _adc_hat:  ADC on the top-board
        @param _shutdown_gpo_def: GPO definition of the power shutdown pin
        @return An instance of the PowerManagement class
        """
        self.__io_handler = _io_handler
        self.__adc_hat = _adc_hat
        self.__shutdown_gpo = _io_handler.get_gpo(_shutdown_gpo_def)

        self.__timerIsRunning = False
        self.__accu_percentage_capacity = 0
        self.__accu_voltage = 0
        self.__accu_capacity_ok = False
        self.__raw_accu_voltages_array = [12.6] * ACCU_CHECK_SIZE_OF_WINDOW     # fills array with default value: 12.6

        self.__signaling_device = None
        self.__shutdown_in_progress = False
        self.__counter_prevent_startup_power_fail = 0

        self.__battery_check_started = False
        self.__to_low_already_display = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def init_power_management(self) -> None:
        """!
        Initializes power management (Mandatory)

        @return None
        """

        self.__timerIsRunning = True

        if self.__adc_hat is not None:
            self.__start_timer_power_management()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def exit_program(self) -> None:
        """!
        Cleans up, when user want to shut down (for future use)

        @return: None
        """
        self.stop_timer_power_management()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __start_timer_power_management(self) -> None:
        """!
        Starts the timer to check the accu voltage

        @return: None
        """
        timer = threading.Timer(Robohat_config.ACCU_INTERVAL_TIME_IN_SECONDS, self.timer_callback)
        if self.__timerIsRunning is True:
            timer.start()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def stop_timer_power_management(self) -> None:
        """!

        Stops monitoring the accu capacity
        @return: None
        """
        self.__timerIsRunning = False
        print("Warning: accu monitor disabled")

    # --------------------------------------------------------------------------------------

    def timer_callback(self) -> None:
        """!
        The actual timer function. Retrieves the voltage of the accu and puts it in the fiter function. Restarts the timer.
        Timer will not restart when ADC is not available

        @return: None
        """

        adc_accu_voltage = self.__adc_hat.get_voltage_of_accu()
        calculated_accu_voltage = adc_accu_voltage * Robohat_config.ACCU_VOLTAGE_ADC_MULTIPLIER
        self.__insert_power_voltage(calculated_accu_voltage)
        self.__start_timer_power_management()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def is_timer_running(self) -> bool:
        """!
        Get information if timer is running

        @return: (bool) True if timer is running
        """
        return self.__timerIsRunning

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_accu_percentage_capacity(self) -> int:
        """!
        Gets percentage of accu capacity in %

        @return: (int) accu percentage
        """
        return self.__accu_percentage_capacity

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_accu_voltage(self) -> float:
        """!
        Get voltage of accu

        @return: accu voltage
        """
        return self.__accu_voltage

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def is_accu_capacity_ok(self) -> bool:
        """!
        Returns True, when accu voltage is above the 'ACCU_VOLTAGE_TO_LOW_THRESHOLD'

        @return: (bool) True, accu is OK
        """
        return self.__accu_capacity_ok

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __insert_power_voltage(self, _raw_accu_voltage: float) -> None:
        """!
        Puts the voltage in a median filter.
        Checks if accu voltage is below a threshold.
        When to low alarm and a message will appear

        @param _raw_accu_voltage: accu voltage in volt
        @return: None
        """

        # shift new value in array
        for index in range(1, ACCU_CHECK_SIZE_OF_WINDOW, 1):
            self.__raw_accu_voltages_array[index - 1] = self.__raw_accu_voltages_array[index]

        self.__raw_accu_voltages_array[ACCU_CHECK_SIZE_OF_WINDOW - 1] = _raw_accu_voltage

        self.__counter_prevent_startup_power_fail += 1
        if self.__counter_prevent_startup_power_fail < ACCU_CHECK_SIZE_OF_WINDOW:
            return

        self.__counter_prevent_startup_power_fail = ACCU_CHECK_SIZE_OF_WINDOW    # prevent overrun

        self.__accu_voltage = statistics.median(map(float, self.__raw_accu_voltages_array)) # create median

        if self.__accu_voltage > 0.5:
            self.__accu_percentage_capacity = self.__calculate_percentage_from_voltage(self.__accu_voltage)
            if self.__accu_voltage < Robohat_config.ACCU_VOLTAGE_TO_LOW_THRESHOLD:
                self.__accu_capacity_ok = False

                if self.__signaling_device is not None:
                    self.__signaling_device.signal_system_alarm()
                    print("power fail alarm triggered")

                if Robohat_config.ACCU_LOG_DISPLAY_WHEN_TO_LOW is True or self.__to_low_already_display is False:
                    print("accu capacity to low, only {0:3.2f} %".format(self.__accu_percentage_capacity))
                    self.__to_low_already_display = True

            elif self.__accu_capacity_ok is False or self.__accu_voltage > Robohat_config.ACCU_VOLTAGE_TO_LOW_THRESHOLD + (Robohat_config.ACCU_VOLTAGE_TO_LOW_THRESHOLD * 0.02):
                self.__accu_capacity_ok = True

        else:
            if self.__battery_check_started is False:
                self.__accu_percentage_capacity = -1

        if self.__battery_check_started is False:
            self.__battery_check_started = True

            print("***********************************")
            print("accu monitor active")
            print("accu voltage: {0:2.2f} V".format(self.__accu_voltage))
            print("accu percentage: {0:3.2f} %".format(self.__accu_percentage_capacity))

            if self.__accu_capacity_ok is True:
                print("accu is OK")
            else:
                print("accu has a too low capacity")
            print("***********************************")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __calculate_percentage_from_voltage(self, _accu_voltage: float) -> float:
        """!
        Calculates voltgae of accu, to accu capacity, derived from array in Robohat_config

        @param _accu_voltage:
        @return: percentage of accu
        """

        # gets percentage out of list, and interpolates the voltages between the elements of the list
        if _accu_voltage <= Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY[0] [0]:
            return 0

        if _accu_voltage >= Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY[len(Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY) - 1] [0]:
            return 100

        for index in range(0, len(Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY) - 1, 1):
            voltage_low = Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY[index] [0]
            voltage_high = Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY[index + 1] [0]

            diff_voltage = voltage_high - voltage_low
            diff_perc = Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY[index + 1] [1] - Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY[index] [1]
            perc_per_volt = diff_perc / diff_voltage

            if voltage_low <= _accu_voltage <= voltage_high:
                remainder_volt = voltage_high - _accu_voltage
                remainder_perc = remainder_volt * perc_per_volt

                percentage = Robohat_config.ACCU_VOLTAGE_TO_PERCENTAGE_ARRAY[index] [1] + remainder_perc
                return percentage

        self.shutdown_power()
        return 0

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def add_signaling_device(self, _signaling_device) -> None:
        """!
        Adds device which will alarms the user

        @param _signaling_device:
        @return: Nome
        """

        self.__signaling_device = _signaling_device

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def shutdown_power(self) -> None:
        """!
        Will toggle the PIO shutdown pin

        @return: None
        """
        if self.__shutdown_in_progress is True:
            return

        print("Power shutdown in 1 minute")

        self.__shutdown_gpo.set_high()
        sleep(5)                            # hold the GPIO pin for 5 seconds (shorter time will not shutdown the accu management board
        self.__shutdown_gpo.set_low()

        self.__io_handler.io_shutdown()
        os.system("sudo shutdown -h now")       # actual system call to shut down the RPi
        print("RPi will shutdown")

        if self.__signaling_device is not None:
            self.__signaling_device.signal_system_alarm()

        self.__shutdown_in_progress = True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
