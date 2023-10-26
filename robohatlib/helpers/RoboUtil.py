"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    from robohatlib.hal.assemblyboard.PwmPlug import PwmPlug
    import time

except ImportError:
    print("Failed to import dependencies for RoboUtil")
    raise

    # -------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------


class RoboUtil:
    """!
    Class with utility functions
    """

    @staticmethod
    def update_byte(_data_byte, _bit_nr, _wanted_bit_value):
        """!
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
    def check_bit(_data_byte, _bit_nr):
        """!
        returns 1 if bit is true in _data_byte of _bit_nr. returns 0 when false. _bit_nr starts at 0

        @param _data_byte the value to be checked
        @param _bit_nr bit nr (starts at 0)
        @return status 0 or 1 (1 if True)
        """

        value = 0
        if _data_byte & (1 << _bit_nr):
            value = 1

        return value

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    @staticmethod
    def print_depending_switch(_silent: bool, _txt: str) -> None:
        """!
        Prints messages to the console depending on the _silent switch

        @param _silent: Switch, True will print the message to console
        @param _txt: The text to print
        @return: None
        """

        if _silent is False:
            print(_txt)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    @staticmethod
    def get_pwmplug_by_int(_id: int) -> PwmPlug:
        """!
        Convert int id to PWMplug enum
        @param _id: id in int
        @return: Pwmplug
        """
        if _id == 1:
            return PwmPlug.PWMPLUG_P4
        else:
            return PwmPlug.PWMPLUG_P3

    # --------------------------------------------------------------------------------------

    @staticmethod
    def get_pwm_cs_by_pwmplug(_plug: PwmPlug) -> int:
        """!
        Convert to PWMplug enum int id
        @param _plug: PWMplug enum
        @return: int id
        """
        if _plug == PwmPlug.PWMPLUG_P4:
            return 1
        else:
            return 0

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    @staticmethod
    def get_time_ms() -> int:
        """!
        Returns current epoch time in milli Seconds
        @return: mS (int)
        """
        return int(time.time() * 1000)
