
"""Module examples"""


import logging
from .arduino import ArduinoObject


class DriveTrain(ArduinoObject):
    """
    Example: drive PWM servo through arduino (8-bit PWM)
    """

    pid = 0x01

    speed = None

    def set_motor(self, speed):
        if speed > 256 or speed < 0:
            logging.error("Attempted to write speed above 256")
            return False

        self.speed = speed
        return True

    def loop(self):
        if self.speed is not None:
            self.send(0x01, bytes([self.speed]))
            self.speed = None

        return True


drive_train = DriveTrain(baudrate=115200)
drive_train.set_motor(0)


class AnalogSensor(ArduinoObject):
    """
    Example: read sensor values
    """

    pid = 0x02
    data_available = False

    def loop(self):
        self.send(0x01, bytes())
        self.first_sensor = self.get()
        self.send(0x02, bytes())
        self.second_sensor = self.get()
        self.data_available = True

        return True


sensor = AnalogSensor(baudrate=115200)
while not sensor.data_available:
    pass
print sensor.first_sensor
print sensor.second_sensor
