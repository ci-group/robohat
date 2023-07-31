#!/usr/bin/python3
try:
    import threading
except ImportError:
    threading = None

try:
    from robohatlib.driver_ll.i2c.VU_SMBUS import VU_SMBUS
except ImportError:
    raise ImportError("SMBus not found.")

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class VU_I2CHandler:
    def __init__(self, _bus_nr: int):
        """!
        Constructor
        @param _bus_nr bus nr
        """

        self._i2c_bus = VU_SMBUS(_bus_nr)
        self._locked = False
        self._lock = threading.RLock()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __enter__(self):
        """!
        Will enter when class is used
        Locks the I2C bus when using i
        """
        if threading is not None:
            self._lock.acquire()
        return self

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):
        """!
        Will enter when function is left
        Releasing the I2C bus when leaving it

        @param exc_type: ?
        @param exc_value: ?
        @param traceback: ?
        @return: ?
        """
        if threading is not None:
            self._lock.release()
            del self._i2c_bus

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def scan(self) -> []:
        """!
        Try to read a byte from each address, if you get an OSError
        it means the device isn't there
        """

        found = []
        for addr in range(0, 0x80):
            try:
                self._i2c_bus.read_byte(addr)
            except OSError:
                continue
            found.append(addr)
        return found

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    def write_bytes(self, _slave_address, buffer) -> None:
        """
        Write multiply bytes to the I2C bus
        @param _slave_address:
        @param buffer:
        @return: None
        """

        self._i2c_bus.write_bytes(_slave_address, buffer)

    # --------------------------------------------------------------------------------------
    def read_from_into(self, address, buffer) -> None:
        """!
        Read data from an address and into the buffer
        """

        length = len(buffer)
        tmp_buffer = self._i2c_bus.read_bytes(address, length)

        # put into buffer given by the user
        for i in range(length):
            buffer[i] = tmp_buffer[i]

    # --------------------------------------------------------------------------------------
    def write_to_then_read_from(self, _slave_address, buffer_out, buffer_in ) -> None:
        """!
        Write bytes to the I2C bus
        Reads bytes to the I2C bus
        """

        self.write_bytes(_slave_address, buffer_out)
        self.read_from_into(_slave_address, buffer_in)

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def try_lock(self) -> bool:
        """!
        Acquire lock and return FALSE if denied
        @return: status of the LOCK
        """

        if self._locked:
            return False
        else:
            self._locked = True
            return True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def unlock(self) -> None:
        """!
        Release lock
        @return: None
        """

        if self._locked:
            self._locked = False
        else:
            raise ValueError("Not locked")

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
