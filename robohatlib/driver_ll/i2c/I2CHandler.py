"""!
Robohatlib (2022-2823-01)
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)
"""

try:
    import threading
    import asyncio

except ImportError:
    threading = None

try:
    from robohatlib.driver_ll.i2c.smbus import SMBUS

except ImportError:
    raise ImportError("SMBus not found.")

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class I2CHandler:
    def __init__(self, _bus_nr: int):
        """!
        Constructor
        @param _bus_nr bus nr
        """

        self._i2c_bus = SMBUS(_bus_nr)
        self._lock = threading.RLock()

        self._sw_lock = False

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

    async def wait_until_unlocked(self) -> bool:
        """!
        Wait until unlocked, and will acquire new lock
        @return: status of the LOCK.
        """

        while self._sw_lock is True:
            await asyncio.sleep(0.001)

        self._sw_lock = True

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def unlock(self) -> None:
        """!
        Release lock
        @return: None
        """

        self._sw_lock = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------