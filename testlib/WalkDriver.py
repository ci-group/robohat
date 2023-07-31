try:
    from robohatlib.Robohat import Robohat
    import time
    import threading
    import time
    from enum import Enum
    from enum import IntEnum

except ImportError:
    print("Failed to import needed dependencies for the WalkDriver class")
    raise

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

class WalkDriver:

    def __init__(self):
        """!
         Constructor
        """
        print("Constructor of WalkDriver")
        self.__running = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def start_walking(self) -> None:
        print("start_walking")

        self.__running = True
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def stop_walking(self) -> None:
        print("stop_walking")

        self.__running = False

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    def run(self):
        while self.__running is True:
            # Do something
            print('Doing something important in the background')

            time.sleep(1)  # wait 100 mS

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

