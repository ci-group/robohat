"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    import spidev
except ImportError:
    raise ImportError("spidev not found.")


class SPIDevice:
    __spi_bus = None
    __spi_cs_nr = 0x00
    __device_name = ""

    def __init__(self, _device_name: str, _spi_bus, _spi_bus_nr: int, _spi_cs_nr: int):
        """!
        @param _device_name:
        @aram _spi_bus:
        @param _spi_bus_nr:
        @param _spi_cs_nr:
        """
        self.__device_name = _device_name
        self.__spi_bus = _spi_bus
        self.__spi_bus_nr = _spi_bus_nr
        self.__spi_cs_nr = _spi_cs_nr

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def get_device_name(self):
        """!
        Return the name of the spi device
        @return: name
        """
        return self.__device_name

    #--------------------------------------------------------------------------------------

    def get_spi_bus(self):
        """!
        Get spi-bus
        @return: spi-bus
        """
        return self.__spi_bus

    #--------------------------------------------------------------------------------------

    def get_spi_bus_nr(self) -> int:
        """!
        Get spi bus nr
        @return: spi bus nr
        """
        return self.__spi_bus_nr

    #--------------------------------------------------------------------------------------

    def get_spi_cs(self) -> int:
        """!

        :return:
        """
        return self.__spi_cs_nr

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------

    def transfer_register(self, data_in):
        """!
        @param data_in:
        @return:
        """

        if self.__spi_bus is None:
            return 0

        data_in_byte_array = data_in.to_bytes(2, "big")
        result_byte_array = self.__spi_bus.xfer(data_in_byte_array)
        resul_int = int.from_bytes(result_byte_array, "big")
        return resul_int

    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------