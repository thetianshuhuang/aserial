
"""Serial device as a python object

Attributes
----------
PORT_ID_CACHE : dict
    Cache of PIDs for each connected serial device
"""

import time
import logging
from .checksum_device import ChecksumDevice
from serial.tools import list_ports


PORT_ID_CACHE = {}


class SerialGetPid(ChecksumDevice):
    """Helper class to get the PID of a device and terminate after receipt"""

    def loop(self):
        """Loop function (overwrites LoopThreading's ``loop`` function"""

        self.send(self, 0x00)

        self.pid = self.get()

        # Exit
        return False


def cache_done(devices):
    """Check if cache assembly has completed

    Returns
    -------
    bool
        ``True`` if all ``SerialGetPid`` objects have finished
    """

    for device in devices:
        if device.done:
            return True
    return False


def refresh_cache(baudrate=115200, timeout=5):
    """Refresh the PID cache

    Parameters
    ----------
    baudrate : int
        Baudrate of the serial devices to connect
    timeout : float
        Time in seconds to try connecting before giving up

    Returns
    -------
    dict
        Port PID cache, once assembled
    """

    devices = {}
    PORT_ID_CACHE = {}

    for port in list_ports.comports():
        devices[port] = SerialGetPid(port, baudrate=baudrate, timeout=timeout)

    while not cache_done:
        # Sleep 10ms
        time.sleep(0.01)

    logging.info("Found " + str(len(devices)) + " serial devices:")
    for name, device in devices.items():
        devices[name] = device.pid
        logging.info(name + " | " + device.pid)

    return PORT_ID_CACHE


# Refresh cache on module load
refresh_cache()


class SerialObject(ChecksumDevice):
    """Serial device as a python object

    Parameters
    ----------
    baudrate : int
        Baudrate of the object
    timeout : float
        Timeout for connection attempts
    """

    def __init__(self, baudrate=115200, timeout=5):

        if not hasattr(self, "pid"):
            logging.error(
                "Arduino object initialized without a PID. No device will " +
                "be connected.")
            return False

        for port, device_pid in PORT_ID_CACHE.items():

            if device_pid == self.pid:
                super().__init__(
                    port, baudrate=baudrate, timeout=timeout)

                logging.info(
                    "Device with pid " + str(self.pid) +
                    " connected at port " + port)

                return True

        return False

    def __str__(self):
        if hasattr(self, "pid"):
            return super().__str__ + " with PID" + self.pid
        else:
            return super().__str__ + " without a registered PID"
