"""
"""


import threading
import logging
import serial


def byte_debug_string(bytestring):
    return(
        "|".join([str(x) for x in bytestring]) +
        " [" + "".join(map(chr, bytestring)) + "]")


class threaded_device(threading.Thread):
    """
    """

    def __init__(self, port, baudrate=115200):

        self.exit_request = False
        self.done = False

        threading.Thread.__init__(self)

        self.port = port
        self.baudrate = baudrate

    def connect(self, timeout):
        """
        """

        try:
            self.device = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=timeout)
            logging.info(
                "Device connected at port " + self.port +
                " at " + str(self.baudrate) + " baud")
            return True

        except serial.serialutil.SerialException:
            logging.warn(
                "Device could not be connected at port " + self.port + ".")
            return False

    def connect_error(self, operation):
        """
        """
        logging.error(
            "Attempted to call '" + operation +
            "' on a closed device " + self.port)

    def close(self):
        """
        """

        if hasattr(self, "device"):
            self.device.close()
            logging.info("Connection to port " + self.port + " closed.")

        return True

    def read(self, chars):
        """
        """
        try:
            return self.device.read(size=chars)
        except serial.serialutil.SerialException:
            self.connect_error("read")
            return None

    def write(self, line):
        """
        """

        try:
            logging.debug(self.port + ".write: " + byte_debug_string(line))
            self.device.write(line)

            return True

        except serial.serialutil.SerialTimeoutException:
            logging.warning(
                "Device " + self.port + " timed out on write")

            return False

        except serial.SerialException:
            self.error("write")

            return False

    def loop(self, exit_request):
        """Main loop to run.

        This method should be overwritten.

        Raises
        ------
        Exception
            This method should NEVER be allowed to run.
        """

        logging.warning(
            "threaded_device instance created without a main loop.")
        raise Exception(
            "threaded_device instance created without a main loop " +
            "(a thread has been created that does nothing)")

        return False

    def main_alive(self):
        """Checks if python's main thread is alive.

        Returns
        -------
        bool
            True if the main thread can be located and is alive; False
            otherwise
        """
        for thread in threading.enumerate():
            if thread.name == "MainThread":
                return(thread.is_alive())

        return False

    def run(self):
        """
        """

        while self.loop(self.exit_request) and self.main_alive():
            pass

        self.done = True
