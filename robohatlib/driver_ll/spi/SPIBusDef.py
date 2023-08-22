"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

class SPIBusDef:
    """!
    Definition of an SPI bus. Here are the SPI pins defined.
    Note. Be sure the SPI bus is defined at the host (such as the RPi)
    """
    def __init__(self, _spi_bus_name: str, _spi_bus_nr: int, _sck_pin: int, _mosi_pin: int, _miso_pin: int):
        """!
        Constructor of the SPI bus definition
        @param _spi_bus_name: name of this definition, just for your own reference
        @param _spi_bus_nr: spi bus nr (should be the nr as called in the host)
        @param _sck_pin: GPIO nr of SCK
        @param _mosi_pin:  GPIO nr of MOSI
        @param _miso_pin: GPIO nr of MISO
        """
        self.__spi_bus_name = _spi_bus_name
        self.__spi_bus_nr = _spi_bus_nr
        self.__sck_pin = _sck_pin
        self.__mosi_pin = _mosi_pin
        self.__miso_pin = _miso_pin

    # --------------------------------------------------------------------------------------

    def get_spi_bus_name(self) -> str:
        """!
        Get the name of this reference
        @return: (str) name
        """
        return self.__spi_bus_name

    # --------------------------------------------------------------------------------------

    def get_spi_bus_nr(self) -> int:
        """!
        Get the SPI bus nr
        @return: (int) spi bus nr
        """
        return self.__spi_bus_nr

    # --------------------------------------------------------------------------------------

    def get_sck_pin(self) -> int:
        """!
        Get SCK pin
        @return: (int) GPIO nr of sck
        """
        return self.__sck_pin

    # --------------------------------------------------------------------------------------

    def get_mosi_pin(self) -> int:
        """!
        Get MOSI pin
        @return: (int) GPIO nr of mosi
        """
        return self.__mosi_pin

    # --------------------------------------------------------------------------------------

    def get_miso_pin(self) -> int:
        """!
        Get MISO pin
        @return: (int) GPIO nr of miso
        """
        return self.__miso_pin

    # --------------------------------------------------------------------------------------
