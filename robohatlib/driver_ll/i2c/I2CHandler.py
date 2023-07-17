try:
    import threading
except ImportError:
    threading = None

try:
    from robohatlib.driver_ll.i2c.smbus import SMBus
except ImportError:
    raise ImportError("SMBus not found.")

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class I2CHandler:
    def __init__(self, _bus_nr:int):
        """!
        @:param _bus_nr bus nr
        """

        self._i2c_bus = SMBus(_bus_nr)
        self._locked = False
        self._lock = threading.RLock()

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __enter__(self):
        """!
        @return: ?
        """
        if threading is not None:
            self._lock.acquire()
        return self

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):
        """!
        Destructor
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

    def write_to(self, address, buffer, *, start=0, end=None, stop=True) -> None:
        """!
        Writes bytes to the I2C bus
        @param address: its address
        @param buffer: buffer
        @param start: start, default 0
        @param end: end, default None
        @stop does nothing, for compatibility present
        @return: none
        """

        if end is None:
            end = len(buffer)
        self._i2c_bus.write_bytes(address, buffer[start:end])

    # --------------------------------------------------------------------------------------

    def read_from_into(self, address, buffer, *, start=0, end=None, stop=True) -> None:
        """!
        Read data from an address and into the buffer
        """

        if end is None:
            end = len(buffer)

        value_in = self._i2c_bus.read_bytes(address, end - start)
        for i in range(end - start):
            buffer[i + start] = value_in[i]
    # --------------------------------------------------------------------------------------

    def write_to_then_read_from(
            self,
            address,
            buffer_out,
            buffer_in,
            *,
            out_start=0,
            out_end=None,
            in_start=0,
            in_end=None,
            stop=False,
    ) -> None:

        """!
        Write data from buffer_out to an address and then
        read data from an address and into buffer_in
        """

        if out_end is None:
            out_end = len(buffer_out)
        if in_end is None:
            in_end = len(buffer_in)
        if stop:
            # To generate a stop in linux, do in two transactions
            self.write_to(address, buffer_out, start=out_start, end=out_end, stop=True)
            self.read_from_into(address, buffer_in, start=in_start, end=in_end)
        else:
            # To generate without a stop, do in one block transaction
            data_in = self._i2c_bus.read_i2c_block_data(address, buffer_out[out_start:out_end], in_end - in_start)
            for i in range(in_end - in_start):
                buffer_in[i + in_start] = data_in[i]

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
