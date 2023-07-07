try:
    import spidev
except ImportError:
    raise ImportError("spidev not found.")



class SPI_Device:

    __spi_bus = None
    __spi_cs_nr = 0x00
    __device_name = ""

    def __init__(self, _device_name, _spi_bus, _spi_bus_nr, _spi_cs_nr):
        self.__device_name = _device_name
        self.__spi_bus = _spi_bus
        self.__spi_bus_nr = _spi_bus_nr
        self.__spi_cs_nr = _spi_cs_nr

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def writeRegister(self, data):
        if (self.__spiADC is None):
            return 0

        dataAsArray = data.to_bytes(2, "big")
        resultAsArray = self.__spi_bus.xfer(dataAsArray)
        resulAsInt = int.from_bytes(resultAsArray, "big")
        return resulAsInt

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def writeRegister(self, data):
        if (self.__spi_bus is None):
            return 0

        dataAsArray = data.to_bytes(2, "big")
        resultAsArray = self.__spi_bus.xfer(dataAsArray)
        resulAsInt = int.from_bytes(resultAsArray, "big")
        return resulAsInt

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_device_name(self):
        return self.__device_name

    #--------------------------------------------------------------------------------------

    def get_spi_bus(self):
        return self.__spi_bus

    #--------------------------------------------------------------------------------------


    def get_spi_bus_nr(self):
        return self.__spi_bus_nr

    #--------------------------------------------------------------------------------------

    def get_spi_cs(self):
        return self.__spi_cs_nr

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------