class SPI_Bus_Definition:

    def __init__(self, _spi_bus_name, _spi_bus_nr, _sck_pin, _mosi_pin, _miso_pin):
        self.__spi_bus_name = _spi_bus_name
        self.__spi_bus_nr = _spi_bus_nr
        self.__sck_pin = _sck_pin
        self.__mosi_pin = _mosi_pin
        self.__miso_pin = _miso_pin


    def get_spi_bus_name(self):
        return self.__spi_bus_name

    #--------------------------------------------------------------------------------------

    def get_spi_bus_nr(self):
        return self.__spi_bus_nr

    #--------------------------------------------------------------------------------------

    def get_sck_pin(self):
        return self.__sck_pin

    #--------------------------------------------------------------------------------------

    def get_mosi_pin(self):
        return self.__mosi_pin

    #--------------------------------------------------------------------------------------

    def get_miso_pin(self):
        return self.__miso_pin

    #--------------------------------------------------------------------------------------