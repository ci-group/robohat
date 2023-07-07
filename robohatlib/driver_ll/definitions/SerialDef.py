class SerialDef:
    def __init__(self, _name, _comm_port):
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

    def get_comm_port(self):
        return self.__comm_port

    # --------------------------------------------------------------------------------------

