try:
    from robohatlib.driver_ll.definitions.LedDef import LedDef
except ImportError:
    print("Failed to import MultiColorLedDef")
    raise




class MultiColorLedDef:

    """!
    Definition for a MultiColorLed Device
    """

    def __init__(self, _name, _red_def, _green_def, _blue_def):
        """
        :param _name: name of this definition
        :param _red_def: definition of the RED LED
        :param _green_def:  definition of the GREEN LED
        :param _blue_def: definition of the BLUE LED
        """
        self.__name = _name
        self.__red_def = _red_def
        self.__green_def = _green_def
        self.__blue_def = _blue_def

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Returns name of this definition

        @return: name of this definition
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_red_def(self) -> LedDef:
        """!
        get definition of the RED LED
        @return: definition of the RED LED
        """
        return self.__red_def

    def get_green_def(self) -> LedDef:
        """!
        get definition of the GREEN LED
        @return: definition of the GREEN LED
        """
        return self.__green_def

    def get_blue_def(self) -> LedDef:
        """!
        get definition of the BLUE LED
        @return: definition of the BLUE LED
        """
        return self.__blue_def

    # --------------------------------------------------------------------------------------

