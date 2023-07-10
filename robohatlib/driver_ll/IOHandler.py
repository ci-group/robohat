#!/usr/bin/python3
from __future__ import annotations

try:
    from robohatlib.driver_ll.GPO_LL_Driver import GPO_LL_Driver
    from robohatlib.driver_ll.GPI_LL_Driver import GPI_LL_Driver
    from robohatlib.driver_ll.GPOPWM_LL_Driver import GPOPWM_LL_Driver
    from robohatlib.driver_ll.GPI_LL_Interrupt import GP_interrupt

    from robohatlib.driver_ll.i2c.I2CDevice import I2CDevice
    from robohatlib.driver_ll.i2c.I2CDeviceDef import I2CDeviceDef

    from robohatlib.driver_ll.definitions.GPIDef import GPIDef
    from robohatlib.driver_ll.definitions.GPODef import GPODef
    from robohatlib.driver_ll.definitions.GPOPWMDef import GPOPWMDef
    from robohatlib.driver_ll.definitions.GPIInterruptDef import GPIInterruptDef

    from robohatlib.driver_ll.i2c.I2CBus import I2CBus
    from robohatlib.driver_ll.i2c.I2CHandler import I2CHandler

    from robohatlib.driver_ll.spi.SPI_Device import SPI_Device
    from robohatlib.driver_ll.spi.SPIDeviceDef import SPIDeviceDef

    from robohatlib.drivers.Led_driver import Led_driver
    from robohatlib.driver_ll.definitions.LedDef import LedDef
    from robohatlib.drivers.Buzzer_driver import Buzzer_driver
    from robohatlib.hal.definitions.BuzzerDef import BuzzerDef

    from robohatlib import Robohat_config
    from robohatlib import Robohat_constants
    from robohatlib.driver_ll.datastructs.IOStatus import IOStatus

except ImportError:
     raise ImportError("Failed to import needed dependencies for the IOHandler class")

try:
    import spidev
except ImportError:
    raise ImportError("spidev not found, needed for IOHandler class")

try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError("GPIO not found, needed for IOHandler class")

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class IOHandler:
    """!
    In this class all low level IO checking and handling are done
    """


    def __init__(self):
        """!
        The IO_Handler base class initializer.

        @return: An instance of the IO_Handler class
        """

        self.__i2c_bus_is_scanned = False
        self.__used_gpio = []
        self.__available_i2c_busses = []
        self.__used_i2c_devices = []
        self.__detected_i2c_devices = []
        self.__available_spi_buses = []
        self.__used_spi_devices = []


    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def init_io(self) -> None:
        """!
        Initializes the IO

        @return: None
        """

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __pre_scan_i2c_bus(self) -> None:
        """!
        Does a I2C bus scam, at init

        @return: None
        """

        if self.__i2c_bus_is_scanned == False:
            self.scan_i2c_bus()
            self.__i2c_bus_is_scanned = True

    #--------------------------------------------------------------------------------------

    def scan_i2c_bus(self) -> None:
        """!
        Scans all the I2C bussed available on the Robohat hardware.
        Displays found I2C devices onto console
        The found devices will be stored in a list. This list will be used when an I2C device is allocated. When the device is allocated and not in this list, an error will occur

        @return: None
        """
 
        print("\nScanning all I2C busses....")

        found = False

        # I2C bus 0 not availble

        print("####################")
        print("I2C1:\n")
        i2c1 = self.__get_i2c_bus(1)
        print("\n")
        found = False
        for addr in i2c1.get_i2c_handler().scan():
            if self.__i2c_bus_is_scanned is False:
                self.__detected_i2c_devices.append(I2CDevice("unknown", i2c1.get_i2c_handler(), 1, addr))
            print("Found I2C_device @ " + hex(addr))
            found = True

        if found is False:
            print("No I2C_device found on this bus")

        print("####################")
        print("I2C5:\n")
        i2c_5 = self.__get_i2c_bus(5)
        print("\n")
        found = False
        for addr in i2c_5.get_i2c_handler().scan():
            if self.__i2c_bus_is_scanned is False:
                self.__detected_i2c_devices.append(I2CDevice("unknown", i2c_5.get_i2c_handler(), 5, addr))
            print("Found I2C_device @ " + hex(addr))
            found = True

        if found is False:
            print("No I2C_device found on this bus")

        print("####################")
        print("I2C6:\n")
        i2c6 = self.__get_i2c_bus(6)
        print("\n")
        found = False
        for addr in i2c6.get_i2c_handler().scan():
            if self.__i2c_bus_is_scanned is False:
                self.__detected_i2c_devices.append(I2CDevice("unknown", i2c6.get_i2c_handler(), 6, addr))
            print("Found I2C_device @ " + hex(addr))
            found = True

        if found is False:
            print("No I2C_device found on this bus")
        print("####################\n")

        # # no deinit, the busses will be used, so no need to deinit them
        # #i2c1.deinit()
        # #i2c5.deinit()
        # #i2c6.deinit()

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_i2c_device(self, _i2c_device_def: I2CDeviceDef) -> I2CDevice | None:
        """!
        allocates the I2C device, when available on the I2C bus (so should be seen in the scan).

        @param _i2c_device_def: configuration of the I2C device. such as: I2C_Device_Definition("IOEXPANDER_I2C", 1, 0x20) ), See class I2C_Device_Definition
        @return: I2C_Device
        """
        self.__pre_scan_i2c_bus()

        if self.__is_i2c_slot_available(_i2c_device_def) is False:
           print("Warning, I2C device: " + _i2c_device_def.get_name() + " is not found I2C bus: " + str(_i2c_device_def.get_i2c_bus_nr()) + " @ address: " + str(_i2c_device_def.get_i2c_device_address()) )
           return None

        i2c_bus = self.__get_i2c_bus(_i2c_device_def.get_i2c_bus_nr() )
        i2c_handler = i2c_bus.get_i2c_handler()

        if len(self.__used_i2c_devices) is not 0:
            for i2c_device_from_list in self.__used_i2c_devices:
                #print("comparing for: " + _i2c_device_def.get_name() + " -> " + str(i2c_device_from_list.get_i2c_bus_nr()) + "<>" + str(_i2c_device_def.get_i2c_bus_nr()) + ", wanted: " + hex(i2c_device_from_list.get_i2c_device_address()) + "<>" + hex(_i2c_device_def.get_i2c_device_address()) )
                if i2c_device_from_list.get_i2c_bus_nr() is _i2c_device_def.get_i2c_bus_nr() and i2c_device_from_list.get_i2c_device_address() is _i2c_device_def.get_i2c_device_address():
                    #print("Device already claimed")
                    raise Exception("I2C device already claimed")

        i2c_device = I2CDevice(_i2c_device_def.get_name() + "_i2c", i2c_handler, _i2c_device_def.get_i2c_bus_nr(), _i2c_device_def.get_i2c_device_address())
        self.__used_i2c_devices.append(i2c_device)
        print("I2C device registered: " + _i2c_device_def.get_name() + " -> i2c_bus:" + str(_i2c_device_def.get_i2c_bus_nr()) + ", address: " + hex(_i2c_device_def.get_i2c_device_address()))
        return i2c_device

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_spi_device(self, _spi_device_def:SPIDeviceDef) -> SPI_Device:
        """!
        Get SPI device

        @param _spi_device_def:
        @return: SPI_Device
        """

        spi_bus_nr = _spi_device_def.get_spi_bus_nr()
        spi_cs = _spi_device_def.get_spi_cs_nr()

        self.__check_spi_bus(spi_bus_nr)                    # will fail when bus has cpnflict with a gpio pin...

        if self.__add_gio_if_not_already_used_or_give_error(spi_cs, _spi_device_def.get_name()) is IOStatus.IO_FAILED:
            raise Exception("Unable to claim SPI "+ str(spi_bus_nr) + ", CS-pin: '" + str(spi_cs) + "', pin is already in use")

        if len(self.__used_spi_devices) is not 0:
            for _deviceinlist in self.__used_spi_devices:
                if _deviceinlist.get_spi_bus_nr() is spi_bus_nr and _deviceinlist.get_spi_cs() is spi_cs:
                    print("SPI device already claimed!!: SPI-bus: " + spi_bus_nr + " cs:" + str(spi_cs))
                    return _deviceinlist

        spi_bus = spidev.SpiDev()
        spi_bus.open(_spi_device_def.get_spi_bus_nr(), _spi_device_def.get_spi_cs_nr())    #_spi_bus_nr, _spi_cs_nr)
        spi_bus.max_speed_hz = _spi_device_def.get_spi_max_speed()
        spi_bus.mode = _spi_device_def.get_spi_mode()                                    # SPI mode as two bit pattern of clock polarity and phase [CPOL|CPHA], min: 0b00 = 0, max: 0b11 = 3
        spi_bus.lsbfirst = False
        spi_device =  SPI_Device(_spi_device_def.get_name(), spi_bus, _spi_device_def.get_spi_bus_nr(), _spi_device_def.get_spi_cs_nr())

        print("SPI device registered: " + _spi_device_def.get_name() + " -> spi_bus:" + str(spi_bus_nr) + ", cs: " + str(spi_cs))
        self.__used_spi_devices.append(spi_device)

        return spi_device

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #todo check if input is really an input pin

    def get_gpi(self,_gpi_definition:GPIDef) -> GPI_LL_Driver:
        """!
        get GPI (general purpose input)

        @param _gpi_definition: gpi definition
        @return: GPI_LL_Driver
        """
        gpio_pin = _gpi_definition.get_gpi_pin_nr()

        if self.__add_gio_if_not_already_used_or_give_error(gpio_pin, _gpi_definition.get_name()) is IOStatus.IO_OK:
            return GPI_LL_Driver(_gpi_definition)
        else:
            raise Exception("Unable to claim GPI-pin: '" + str(gpio_pin) + "', the GPI-pin is already in use")

    # --------------------------------------------------------------------------------------
    def get_gpo(self, _gpo_definition:GPODef) -> GPO_LL_Driver:
        # todo check if output is really an output pin

        """!
        get GPO (general purpose output)

        @param _gpo_definition:
        @return: GPO_LL_Driver
        """
        gpio_pin = _gpo_definition.get_gpo_pin_nr()

        if self.__add_gio_if_not_already_used_or_give_error(gpio_pin, _gpo_definition.get_name() ) is IOStatus.IO_OK:
            return GPO_LL_Driver(_gpo_definition)
        else:
            raise Exception("Unable to claim GPO-pin: '" + str(gpio_pin) + "', the GPO-pin is already in use")
    #--------------------------------------------------------------------------------------

    #todo make it shareable!!
    def register_interrupt(self, _gpi_interrupt_definition:GPIInterruptDef) -> GP_interrupt | None:
        """!
        registers interrupt

        @param _gpi_interrupt_definition:
        @return: GP_interrupt
        """
        if _gpi_interrupt_definition is None:
            return None

        return GP_interrupt(_gpi_interrupt_definition)

    #--------------------------------------------------------------------------------------

    def get_pwm(self, _gpopwm_definition:GPOPWMDef) -> GPOPWM_LL_Driver:
        """!
        Get PWM

        @param _gpopwm_definition:
        @return: GPOPWM_LL_Driver
        @raises: Exception
        """
        gpio_pin = _gpopwm_definition.get_gpo_pin_nr()

        if self.__add_gio_if_not_already_used_or_give_error(gpio_pin, _gpopwm_definition.get_name()) is IOStatus.IO_OK:
            return GPOPWM_LL_Driver(_gpopwm_definition)
        else:
            raise Exception("Unable to claim PWM-pin: '" + str(gpio_pin) + "', the PWM-pin is already in use")

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_led_driver(self, _led_def:LedDef) -> Led_driver:
        """!
        Get LED driver

        @param _led_def:
        @return: Led
        """

        gpodef = GPODef(_led_def.get_name(), _led_def.get_gpo_pin_nr())

        gpo_ll_driver = self.get_gpo(gpodef)                  # gpo_def had the same functions of led_def
        return Led_driver(gpo_ll_driver)

    #--------------------------------------------------------------------------------------

    def get_buzzer_driver(self, _buzzer_def: BuzzerDef) -> Buzzer_driver:
        """!
        Get Buzzer driver

        @param _buzzer_def:
        @return: Buzzer_driver
        """

        gpopwmdef = GPOPWMDef(_buzzer_def.get_name(), _buzzer_def.get_gpo_pin_nr(), _buzzer_def.get_freq(), _buzzer_def.get_duty_cycle())
        gpopwm_ll_driver = self.get_pwm(gpopwmdef)            # gpopwm_def had the same functions of _buzzer_def
        return Buzzer_driver(gpopwm_ll_driver)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def io_shutdown(self) ->None:
        """@
        shuts down the IO

        @return: None
        """

        GPIO.cleanup()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def __is_i2c_slot_available(self, _to_be_checked:I2CDeviceDef) -> bool:
        """!
        Check if I2C is detected on the bus (list was generated with

        @param _to_be_checked: I2CDeviceDef to be checked i2c_scan
        @return bool:, true if available
        """

        if self.__i2c_bus_is_scanned is False:  # there should always be scanned
            raise Exception("Fatal error, an I2C scan should always be done, before checking if an device is available")

        if len(self.__detected_i2c_devices) is not 0:
            for i2c_device_from_list in self.__detected_i2c_devices:
                available_device:I2CDevice = i2c_device_from_list
                if _to_be_checked.get_i2c_bus_nr() is available_device.get_i2c_bus_nr() and _to_be_checked.get_i2c_device_address() is available_device.get_i2c_device_address():
                    return True

        return False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def is_i2c_device_available(self, _to_be_checked:I2CDeviceDef) -> bool:
        """!
        @param _to_be_checked: I2CDeviceDef to be checked
        @return bool:, true if available
        """

        if len(self.__used_i2c_devices) is not 0:
            for i2c_device_from_list in self.__used_i2c_devices:
                available_device:I2CDevice = i2c_device_from_list
                if _to_be_checked.get_i2c_bus_nr() is available_device.get_i2c_bus_nr() and _to_be_checked.get_i2c_device_address() is available_device.get_i2c_device_address():
                    return True

        return False

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __allocate_i2c_handler(self, _i2c_bus_nr:int, _scl_pin:int, _sda_pin:int, _freq:int=100000) -> I2CHandler:
        """
        :param _i2c_bus_nr:
        :param _scl_pin:
        :param _sda_pin:
        :param _freq:
        :return: I2C_Handler
        :raises: Exception
        """
        if self.__add_gio_if_not_already_used_or_give_error(_scl_pin, "scl") is IOStatus.IO_FAILED:
            raise Exception("Unable to claim I2C "+ str(_i2c_bus_nr) + ", SCL-pin: '" + str(_scl_pin) + "', pin is already in use")

        if self.__add_gio_if_not_already_used_or_give_error(_sda_pin, "sda") is IOStatus.IO_FAILED:
            raise Exception("Unable to claim I2C "+ str(_i2c_bus_nr) + ", SDA-pin: '" + str(_sda_pin) + "', pin is already in use")

        return I2CHandler(_i2c_bus_nr)                # <-- answers to 0x70 which is a ghost device?

        #return busio.I2C(_scl_pin, _sda_pin, _freq)

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def __claim_i2c_bus(self, _i2c_bus_nr:int) -> I2CBus:
        """
        :param _i2c_bus_nr:
        :return: I2C_Bus
        :raises: Exception
        """
        if _i2c_bus_nr is 1:
            def_i = Robohat_config.I2C1_DEF
            i2c_handler_1 = self.__allocate_i2c_handler(def_i.get_i2c_bus_nr(), def_i.get_scl_pin(), def_i.get_sda_pin(), def_i.get_frequency())
            i2c_bus_1 = I2CBus(_i2c_bus_nr, i2c_handler_1)
            self.__available_i2c_busses.append(i2c_bus_1)
            return i2c_bus_1

        elif _i2c_bus_nr is 5:
            def_i = Robohat_config.I2C5_DEF
            i2c_handler_5 = self.__allocate_i2c_handler(def_i.get_i2c_bus_nr(), def_i.get_scl_pin(), def_i.get_sda_pin(), def_i.get_frequency())
            i2c_bus_5 = I2CBus(_i2c_bus_nr, i2c_handler_5)
            self.__available_i2c_busses.append(i2c_bus_5)
            return i2c_bus_5

        elif _i2c_bus_nr is 6:
            def_i = Robohat_config.I2C6_DEF
            i2c_handler_6 = self.__allocate_i2c_handler(def_i.get_i2c_bus_nr(), def_i.get_scl_pin(), def_i.get_sda_pin(), def_i.get_frequency())
            i2c_bus_6 = I2CBus(_i2c_bus_nr, i2c_handler_6)
            self.__available_i2c_busses.append(i2c_bus_6)
            return i2c_bus_6

        raise Exception("Unable to claim I2C-bus " + str(_i2c_bus_nr) )

    # --------------------------------------------------------------------------------------

    def __get_i2c_bus(self, _i2c_bus_nr:int) -> I2CBus:
        """!
        @param _i2c_bus_nr:
        @return: I2CBus
        """
        if len(self.__available_i2c_busses) is not 0:
            for i2c_bus in self.__available_i2c_busses:
                if i2c_bus.get_i2c_bus_nr() is _i2c_bus_nr:
                    return i2c_bus

        return self.__claim_i2c_bus(_i2c_bus_nr)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __check_pinning_spi_bus(self, _spi_bus_nr:int, _sck_pin:int, _mosi_pin:int, _miso_pin:int) -> None:
        """!
        @param _spi_bus_nr:
        @param _sck_pin:
        @param _mosi_pin:
        @param _miso_pin:
        @return: None
        """
        if self.__add_gio_if_not_already_used_or_give_error(_sck_pin, "sck") is IOStatus.IO_FAILED:
            raise Exception("Unable to claim SPI "+ str(_spi_bus_nr) + ", SCK-pin: '" + str(_sck_pin) + "', pin is already in use")

        if self.__add_gio_if_not_already_used_or_give_error(_mosi_pin, "mosi") is IOStatus.IO_FAILED:
            raise Exception("Unable to claim SPI "+ str(_spi_bus_nr) + ", MOSI-pin: '" + str(_mosi_pin) + "', pin is already in use")

        if self.__add_gio_if_not_already_used_or_give_error(_miso_pin, "miso") is IOStatus.IO_FAILED:
            raise Exception("Unable to claim SPI "+ str(_spi_bus_nr) + ", MISO-pin: '" + str(_miso_pin) + "', pin is already in use")

    # --------------------------------------------------------------------------------------

    def __check_spi_bus(self, _spi_bus_nr:int) -> None:
        """!
        @param _spi_bus_nr:
        @return: None
        """
        if len(self.__available_spi_buses) is not 0:
            for spibusnr_already_checked in self.__available_spi_buses:
                if spibusnr_already_checked is _spi_bus_nr:
                    print("SPI already checked!!: " + str(_spi_bus_nr))
                    return

        if _spi_bus_nr is 0:
            def_i = Robohat_config.SPI0_DEF
            self.__check_pinning_spi_bus(def_i.get_spi_bus_nr(), def_i.get_sck_pin(), def_i.get_mosi_pin(), def_i.get_miso_pin())
            self.__available_spi_buses.append(_spi_bus_nr)

        elif _spi_bus_nr is 1:
            def_i = Robohat_config.SPI1_DEF
            self.__check_pinning_spi_bus(def_i.get_spi_bus_nr(), def_i.get_sck_pin(), def_i.get_mosi_pin(), def_i.get_miso_pin())
            self.__available_spi_buses.append(_spi_bus_nr)

        elif _spi_bus_nr is 2:
            def_i = Robohat_config.SPI2_DEF
            self.__check_pinning_spi_bus(def_i.get_spi_bus_nr(), def_i.get_sck_pin(), def_i.get_mosi_pin(), def_i.get_miso_pin())
            self.__available_spi_buses.append(_spi_bus_nr)

        else:
            raise Exception("Unable to claim SPI-bus " + str(_spi_bus_nr) )

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __add_gio_if_not_already_used_or_give_error(self, _gpio_nr: int, _name:str) -> IOStatus:
        """!
        @param _gpio_nr:
        @param _name:
        @return: IOStatus
        """
        #print("checking gpio: " + str(_gpionnr) )

        if len(self.__used_gpio) is 0:
            self.__used_gpio.append(_gpio_nr)
            print("claimed: gpio " + str(_gpio_nr) + " for: " + _name)
            return IOStatus.IO_OK

        for gp in self.__used_gpio:
            if gp == _gpio_nr:
                print("already claimed: gpio " + str(_gpio_nr) + " for: " + _name)
                return IOStatus.IO_FAILED

        self.__used_gpio.append(_gpio_nr)
        print("claimed: gpio " + str(_gpio_nr) + " for: " + _name)
        return IOStatus.IO_OK

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------