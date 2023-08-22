"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

class SPIDeviceDef:
    def __init__(self, _name, _spi_bus_nr, _spi_cs_nr, _max_speed_hz = 8000000, _mode = 0b11):
        self.__name = _name
        self.__spi_bus_nr = _spi_bus_nr
        self.__spi_cs_nr = _spi_cs_nr
        self.__max_speed_hz = _max_speed_hz
        self.__mode = _mode

    # --------------------------------------------------------------------------------------

    def get_name(self):
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_spi_bus_nr(self):
        return self.__spi_bus_nr

    # --------------------------------------------------------------------------------------

    def get_spi_cs_nr(self):
        return self.__spi_cs_nr

    # --------------------------------------------------------------------------------------

    def get_spi_max_speed(self):
        return self.__max_speed_hz

    # --------------------------------------------------------------------------------------

    def get_spi_mode(self):
        return self.__mode

    # --------------------------------------------------------------------------------------

