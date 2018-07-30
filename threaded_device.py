
"""Threaded serial device base class"""


import logging
import serial
from .loop_thread import LoopThreading


def byte_debug_string(bytestring):
    """Print a byte string and its UTF-8 / ASCII representation for logging
    and debugging.

    Parameters
    ----------
    bytestring : bytes
        Python bytes object

    Returns
    -------
    str
        Byte string integer values separated by pipes; ASCII representation
        to the side

        Example::
            97|115|100|102 [asdf]
    """
    return(
        "|".join([str(x) for x in bytestring]) +
        " [" + "".join(map(chr, bytestring)) + "]")


class ThreadedDevice(LoopThreading):
    """Multi-threaded serial device class

    Parameters
    ----------
    port : str
        Port to connect the device to
    baudrate : int
        Baudrate of the serial device

    Attributes
    ----------
    exit_request : bool
        Set to ``True`` in order to request termination; the thread will
        self-terminate on completion of the next main loop iteration
    done : bool
        Is set to ``True`` once the thread exits
    """

    def __init__(self, port, baudrate=115200):

        super().__init__

        self.exit_request = False
        self.done = False
        self.port = port
        self.baudrate = baudrate

    def __str__(self):

        if hasattr(self, "device"):
            if self.device.is_open:
                return "Connected serial device at port " + self.port
            else:
                return "Disconnected serial device at port " + self.port

        else:
            return "Unbound serial device"

    def connect(self, timeout):
        """Connect a serial device to the current port with the given timeout

        Parameters
        ----------
        timeout : float
            Timeout, in seconds, to attempt connection before giving up

        Returns
        -------
        bool
            ``True`` if successful; ``False`` if unsuccessful
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
        """Display a connection error

        This method is called whenever an ``operation`` is called that
        requires a device connection when no device is connected.

        Parameters
        ----------
        operation : str
            Name of the errored operation
        """
        logging.error(
            "Attempted to call '" + operation +
            "' on a closed device " + self.port)

    def close(self):
        """Close the current connection.

        Returns
        -------
        bool
            True (always true currently)
        """

        if hasattr(self, "device"):
            self.device.close()
            logging.info("Connection to port " + self.port + " closed.")

        return True

    def read(self, chars):
        """Read from the serial buffer

        Parameters
        ----------
        chars : int
            Number of bytes to read

        Returns
        -------
        bytes
            Bytes read; ``None`` if unsuccessful
        """
        try:
            return self.device.read(size=chars)
        except serial.serialutil.SerialException:
            self.connect_error("read")
            return None

    def write(self, line):
        """Write to the serial device

        Parameters
        ----------
        line : bytes
            Bytes to write

        Returns
        -------
        bool
            ``True`` if successful; ``False`` otherwise
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
