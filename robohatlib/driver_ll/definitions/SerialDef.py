#!/usr/bin/python3
class SerialDef:
    def __init__(self, _name: str, _comm_port: int):
        """!
        Constructor
        @param _name:
        @param _comm_port:
        """
        self.__name = _name
        self.__comm_port = _comm_port

    # --------------------------------------------------------------------------------------

    def get_name(self) -> str:
        """!
        Returns name of this definition
        @return: name of this definition
        """
        return self.__name

    # --------------------------------------------------------------------------------------

    def get_comm_port(self) -> int:
        return self.__comm_port

    # --------------------------------------------------------------------------------------

