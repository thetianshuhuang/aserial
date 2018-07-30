import serial
import threading
from serial.tools import list_ports


PORT_ID_CACHE = {}


def refresh_cache():

    for port in list_ports.comports():
        print(port)

        # send 0x00
        # get response
        # save to PORT_ID_CACHE

    return PORT_ID_CACHE


# Refresh cache on module load
refresh_cache()

