
"""
0x00 | OPCODE | LENGTH | MSG | CHK
"""

from . import threaded_device
import logging


class Arduino(threaded_device.ThreadedDevice):
    """
    """

    def __init__(self, port, baudrate=115200, timeout=5):

        super().__init__(port, baudrate=baudrate)

        if not self.connect(timeout):
            self.exit_request = True

    def make_chk(self, message):
        """
        """

        chk = message[0]
        for char in message:
            chk ^= char

        return chk

    def send(self, opcode, body):
        """
        """

        return self.write(
            bytes[0, opcode] + body +
            bytes[self.make_chk(body) ^ opcode])

    def get(self):
        """
        """

        length = self.read(1)

        msg = self.read(length)

        if msg[-1] != length ^ self.make_chk(msg[:-1]):
            logging.warning(
                "Checksum does not match message contents")
        else:
            return msg[:-1]
