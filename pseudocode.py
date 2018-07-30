
import serial


# Global cache
CACHED_DEVICE_CODES = {}


class Arduino:

    # Placeholder
    code = 0x00

    def __init__(self, code):

        block here
        for device in serial.tools.list_ports.comports:

            try:
                connect
            finally:
                send 0x00
                if response == code:
                    this.object = created object
                    return success
            except connection error:
                pass

        return failure
        end block

    def close:
        close serial connection

    def build_message(self, *args):
        build arguments

    def send(self, message)
        send to device

    def refresh:
        rerun init


class DriveTrain(Arduino):

    code = <code goes here>

    def move(self, ex)
        send(self, args)

