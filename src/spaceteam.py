import machine

from hardware.pin_manager import PinManager
from logging.pin_logger import PinLogger
from logging.log import Log


class SpaceTeam:

    def __init__(self):
        Log.severity = Log.Severity.DEBUG

        sda = 16
        scl = 17
        freq = 400000
        self.i2c = machine.I2C(0, sda=machine.Pin(sda), scl=machine.Pin(scl), freq=freq)
        Log.debug(f"Initialized I2C with SDA:{sda}, SCL:{scl}, at Frequency:{freq}")

        self.pin_manager = PinManager(self.i2c)
        self.pin_logger = PinLogger()

        self.running = True

    def run(self):
        while self.running:
            self.loop()

    def loop(self):
        pass
