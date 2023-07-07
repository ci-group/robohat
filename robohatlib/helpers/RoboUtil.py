

class RoboUtil:


    '''
    returns new byte value of databyte with wanted boolean value of bitnr , bitnr starts at 0
    '''

    @staticmethod
    def updatebyte(_databyte, _bitnr, _wantedbitvalue):
        """
        :param _databyte:
        :param _bitnr:
        :param _wantedbitvalue:
        :return:
        """
        if _wantedbitvalue < 0 or _wantedbitvalue > 1:
            raise ValueError("value out of range: 0 or 1")

        if _wantedbitvalue == 0:
            return _databyte & ~(1 << _bitnr)
        elif _wantedbitvalue == 1:
            return _databyte | (1 << _bitnr)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    '''
    returns 1 if bit is true in databyte of bitnr. returns 0 when false. bitnr starts at 0
    '''

    @staticmethod
    def checkbit(_databyte, _bitnr):
        value = 0
        if _databyte & (1 << _bitnr):
            value = 1
        return value


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------