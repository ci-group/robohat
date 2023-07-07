

class RoboUtil:
    """
    Class will handy utility functions
    """

    @staticmethod
    def updatebyte(_data_byte, _bit_nr, _wanted_bit_value):
        """
        returns new byte value of _data_byte with wanted boolean value of _bit_nr , _bit_nr starts at 0
        @param _data_byte: initial byte value
        @param _bit_nr: bit nr (starts at 0)
        @param _wanted_bit_value: value of the bit (0 or 1)
        @return: (byte) return value
        """
        if _wanted_bit_value < 0 or _wanted_bit_value > 1:
            raise ValueError("value out of range: 0 or 1")

        if _wanted_bit_value == 0:
            return _data_byte & ~(1 << _bit_nr)
        elif _wanted_bit_value == 1:
            return _data_byte | (1 << _bit_nr)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    @staticmethod
    def checkbit(_data_byte, _bit_nr):
        """
        returns 1 if bit is true in _data_byte of _bit_nr. returns 0 when false. _bit_nr starts at 0

        @param _data_byte the value to be checked
        @param _bit_nr bit nr (starts at 0)
        #return status
        """

        value = 0
        if _data_byte & (1 << _bit_nr):
            value = 1
        return value


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------