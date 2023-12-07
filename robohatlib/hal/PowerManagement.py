"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    import time
    import threading
    import statistics
    import subprocess
    import os
    from time import sleep
    from robohatlib import RobohatConfig
    from robohatlib.driver_ll.definitions.GPODef import GPODef
    from robohatlib.hal.TopboardADC import TopboardADC
    from robohatlib.driver_ll.IOHandler import IOHandler
    from robohatlib.hal.datastructure.BatteryStatus import BatteryStatus

except ImportError:
    print("Failed to import needed dependencies for the PowerManagement class")
    raise


ACCU_CHECK_SIZE_OF_WINDOW = 5

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


class PowerManagement:

    """!
    Class to measure the battery capacity
    """

    def __init__(self, _io_handler: IOHandler, _adc_hat: TopboardADC, _shutdown_gpo_def: GPODef):
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
        self.__battery_percentage_capacity = 0
        self.__battery_voltage = 0
        self.__battery_status = BatteryStatus.UNKNOWN
        self.__raw_battery_voltages_list = [12.6] * ACCU_CHECK_SIZE_OF_WINDOW     # fills a list with default value: 12.6

        self.__signaling_device = None
        self.__shutdown_in_progress = False
        self.__counter_prevent_startup_power_fail = 0

        self.__battery_check_started = False
        self.__to_low_already_displayed = False
        self.__to_high_already_display = False

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

    def exit_program(self, dp_msg:bool = True) -> None:
        """!
        Cleans up, when user want to shut down (for future use)

        @return: None
        """
        self.__stop_timer_power_management(dp_msg)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __start_timer_power_management(self) -> None:
        """!
        Starts the timer to check the battery voltage

        @return: None
        """
        timer = threading.Timer(RobohatConfig.ACCU_INTERVAL_TIME_IN_SECONDS, self.timer_callback)
        if self.__timerIsRunning is True:
            timer.start()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __stop_timer_power_management(self, do_msg: bool = True) -> None:
        """!

        Stops monitoring the battery capacity
        @return: None
        """
        self.__timerIsRunning = False

        if do_msg is True:
            print("Warning: battery monitor disabled")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def timer_callback(self) -> None:
        """!
        The actual timer function. Retrieves the voltage of the battery and puts it in the fiter function. Restarts the timer.
        Timer will not restart when ADC is not available

        @return: None
        """

        adc_battery_voltage = self.__adc_hat.get_voltage_of_battery()

        calculated_battery_voltage = (adc_battery_voltage * RobohatConfig.ACCU_VOLTAGE_ADC_FORMULA_A) + RobohatConfig.ACCU_VOLTAGE_ADC_FORMULA_B
        self.__insert_power_voltage(calculated_battery_voltage)
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

    def get_battery_percentage_capacity(self) -> int:
        """!
        Gets percentage of battery capacity in %

        @return: (int) battery percentage
        """
        return self.__battery_percentage_capacity

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_battery_voltage(self) -> float:
        """!
        Get voltage of battery

        @return: battery voltage
        """
        return self.__battery_voltage

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def get_battery_status(self) -> BatteryStatus:
        """!
        Returns status ot the battery depending on thresholds,  'ACCU_VOLTAGE_TO_LOW_THRESHOLD' and 'ACCU_VOLTAGE_TO_HIGH_THRESHOLD'

        @return: BatteryStatus
        """
        return self.__battery_status

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __insert_power_voltage(self, _raw_battery_voltage: float) -> None:
        """!
        Puts the voltage in a median filter.
        Checks if battery voltage (out of the filter) is below the threshold (ACCU_VOLTAGE_TO_LOW_THRESHOLD).
        When the voltage is 'too low' an alarm and a message will appear

        @param _raw_battery_voltage: battery voltage in volt
        @return: None
        """


        # shift new value in array
        for index in range(1, ACCU_CHECK_SIZE_OF_WINDOW, 1):
            self.__raw_battery_voltages_list[index - 1] = self.__raw_battery_voltages_list[index]

        self.__raw_battery_voltages_list[ACCU_CHECK_SIZE_OF_WINDOW - 1] = _raw_battery_voltage

        self.__counter_prevent_startup_power_fail += 1
        if self.__counter_prevent_startup_power_fail < ACCU_CHECK_SIZE_OF_WINDOW:
            return

        self.__counter_prevent_startup_power_fail = ACCU_CHECK_SIZE_OF_WINDOW    # prevent overrun
        self.__battery_voltage = statistics.median(map(float, self.__raw_battery_voltages_list)) # create median

        if self.__battery_voltage > 0.5:
            self.__battery_percentage_capacity = self.__calculate_percentage_from_voltage(self.__battery_voltage)

#----------------------------- check to low, if so, do shutdown !!!
            if self.__battery_voltage < RobohatConfig.ACCU_VOLTAGE_TO_LOW_THRESHOLD:
                self.__battery_status = BatteryStatus.TOO_LOW

                if self.__signaling_device is not None:
                    self.__signaling_device.signal_system_alarm("Battery voltage too low")

                if self.__to_low_already_displayed is False:
                    print("Battery capacity to low, only {0:3.2f} %".format(self.__battery_percentage_capacity))
                    self.__to_low_already_displayed = True
                    self.shutdown_power()
 # --------------------------------- check if to high, if so do warning. Reset when threshold is met
            elif self.__battery_voltage > RobohatConfig.ACCU_VOLTAGE_TO_HIGH_THRESHOLD:
                self.__battery_status = BatteryStatus.TOO_HIGH

                if self.__signaling_device is not None:
                    self.__signaling_device.signal_system_alarm("Battery voltage too high")

                if RobohatConfig.ACCU_LOG_DISPLAY_WHEN_TO_HIGH is True or self.__to_high_already_display is False:
                    print("Unable to calculate battery, it's above 100 %")
                    self.__to_high_already_display = True

 # check if hysteresis parameters are met when was too high
            elif self.__battery_status is BatteryStatus.TOO_HIGH and \
                    self.__battery_voltage > RobohatConfig.ACCU_VOLTAGE_TO_LOW_THRESHOLD and \
                    self.__battery_voltage < RobohatConfig.ACCU_VOLTAGE_TO_HIGH_THRESHOLD - (RobohatConfig.ACCU_VOLTAGE_TO_HIGH_THRESHOLD * 0.02) :
                self.__battery_status = BatteryStatus.OK
#WARNING 15 present-------------------------------------------------------
            elif self.__battery_percentage_capacity < RobohatConfig.ACCU_WARNING_PERCENTAGE_1 and self.__battery_status is not BatteryStatus.WARNING_1:   # 15
                self.__battery_status = BatteryStatus.WARNING_1
                print("Battery is getting low on capacity. Only " + str(RobohatConfig.ACCU_WARNING_PERCENTAGE_1) + " %")
                if self.__signaling_device is not None:
                    self.__signaling_device.signal_system_alarm("Battery is getting low on capacity")

#WARNING 20 present-------------------------------------------------------
            elif self.__battery_percentage_capacity < RobohatConfig.ACCU_WARNING_PERCENTAGE_2 and self.__battery_status is not BatteryStatus.WARNING_2:            # 20
                self.__battery_status = BatteryStatus.WARNING_2
                print("Battery is getting low on capacity. Only " + str(RobohatConfig.ACCU_WARNING_PERCENTAGE_2) + " %")
                if self.__signaling_device is not None:
                    self.__signaling_device.signal_system_alarm("Battery is getting low on capacity")

            elif self.__battery_status is BatteryStatus.UNKNOWN:
                self.__battery_status = BatteryStatus.OK

        else:
            if self.__battery_check_started is False:
                self.__battery_percentage_capacity = -1
                self.__battery_status = BatteryStatus.ACCU_NOT_PRESENT

        if self.__battery_check_started is False:
            self.__battery_check_started = True

            print("***********************************")
            print("Battery monitor active")
            print("Battery voltage: {0:2.2f} V".format(self.__battery_voltage))
            print("Battery percentage: {0:3.2f} %".format(self.__battery_percentage_capacity))

            if self.__battery_status is BatteryStatus.OK:
                print("Battery is OK")
            elif self.__battery_status is BatteryStatus.TOO_LOW:
                print("Battery has a too low capacity")
            elif self.__battery_status is BatteryStatus.TOO_HIGH:
                print("Battery voltage is to high")
            else:
                print("unknown battery status")
            print("***********************************")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # noinspection PyMethodMayBeStatic
    def __calculate_percentage_from_voltage(self, _battery_voltage: float) -> float:
        """!
        Calculates voltage of battery, to battery capacity, derived from a list in Robohat_config

        @param _battery_voltage:
        @return: percentage of accu
        """

        # gets percentage out of list, and interpolates the voltages between the elements of the list
        if _battery_voltage <= RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST[0] [0]:
            return 0

        if _battery_voltage >= RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST[len(RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST) - 1] [0]:
            return 100

        for index in range(0, len(RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST) - 1, 1):
            voltage_low = RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST[index] [0]
            voltage_high = RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST[index + 1] [0]

            diff_voltage = voltage_high - voltage_low
            diff_perc = RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST[index + 1] [1] - RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST[index] [1]

            if diff_voltage != 0:
                perc_per_volt = diff_perc / diff_voltage

                if voltage_low <= _battery_voltage <= voltage_high:
                    remainder_volt = voltage_high - _battery_voltage
                    remainder_perc = remainder_volt * perc_per_volt

                    percentage = RobohatConfig.ACCU_VOLTAGE_TO_PERCENTAGE_LIST[index] [1] + remainder_perc
                    return percentage

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

        print("Going to power down in 1 minute")

        #removed 7-12-23
        self.__shutdown_gpo.set_high()
        sleep(5)                            # hold the GPIO pin for 5 seconds (shorter time will not shut down the accu management board
        self.__shutdown_gpo.set_low()

        self.__io_handler.io_shutdown()
        os.system("sudo shutdown -h now")       # actual system call to shut down the RPi
        print("RPi will shutdown")

        if self.__signaling_device is not None:
            self.__signaling_device.signal_system_alarm("System shutdown in progress")

        self.__shutdown_in_progress = True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def shutdown_pin_triggered(self) -> None:
        """!
        Is called when IO pin 0 from io_expander is changed
        Will perform shutdown
        """

        print("Shutdown is triggered...")
        #self.shutdown_power()              // disabled, the trigger is nog tested


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
