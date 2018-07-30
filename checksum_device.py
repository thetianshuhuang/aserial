
"""Checksum-based serial device communication wrapper

Protocol::
    0x00 | LENGTH | MSG | CHK
    0x00 | OPCODE | MSG | CHK

- 0x00 must prefix each message
- LENGTH / OPCODE: 8-bit integer; length of the message or called opcode
(designates the target function)
- MSG: bytestring, with length ``LENGTH``; must be shorter than 255 bytes
- CHK: 8-bit checksum; checksum includes ``LENGTH`` and ``MSG``
"""

from . import threaded_device
import logging


class ChecksumDevice(threaded_device.ThreadedDevice):
    """Threaded serial device with checksum communication

    Parameters
    ----------
    port : str
        Port; passed on to ThreadedDevice
    baudrate : int
        Serial baudrate; passed on to ThreadedDevice
    timeout : float
        Connection timeout
    """

    def __init__(self, port, baudrate=115200, timeout=5):

        super().__init__(port, baudrate=baudrate)

        if not self.connect(timeout):
            self.exit_request = True

    def make_chk(self, message):
        """Make the checksum for a message

        Parameters
        ----------
        message : Bytes
            Bytestring to make a checksum for

        Returns
        -------
        chk : int
            Computed XOR checksum of the message
        """

        chk = message[0]
        for char in message:
            chk ^= char

        return chk

    def send(self, opcode, body):
        """Send a message to the connected device

        Parameters
        ----------
        opcode : int
            Opcode to call
        body : bytes
            Bytes to send as the body of the call; the caller must verify
            that ``body`` has the correct length.

        Returns
        -------
        bool
            ``True`` if successful; ``False`` otherwise
        """

        return self.write(
            bytes[0, opcode] + body +
            bytes[self.make_chk(body) ^ opcode])

    def get(self):
        """Get a response from the serial device

        Returns
        -------
        bytes
            Returned byte array; ``None`` if an error occured
        """

        length = self.read(1)

        msg = self.read(length)

        if msg[-1] != length ^ self.make_chk(msg[:-1]):
            logging.warning(
                "Checksum does not match message contents")
            return None
        else:
            return msg[:-1]
