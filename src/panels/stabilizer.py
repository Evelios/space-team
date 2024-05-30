from machine import I2C
from hardware.pin_manager import PinManager
from enum import Enum, auto

# from display.pico_i2c_lcd import I2cLcd
from sensor.rotary_encoder import RotaryEncoder


class Stabilizer:
    """
    Stabilizer panel
    """

    class Event(Enum):
        POSITION_CHANGE = auto()
        UNSTABLE = auto()
        CRASH = auto()

    stability = 0
    """Stability of this device. Range -1 -> 1"""

    rotary_encoder = RotaryEncoder
    """stabilizer_input"""
    previous_reading = 0

    def __init__(self, i2c: I2C, p1: int, p2: int, p3: int, p4: int):
        self.i2c = i2c
        self.rotary_encoder = RotaryEncoder(p1, p2, p3, p4)

    def update(self):
        encoder_reading = self.rotary_encoder.read()

        if encoder_reading == self.previous_reading:
            return

        self.stability += self.previous_reading - encoder_reading
        self.previous_reading = encoder_reading

    # ---- Event Handling ----------------------------------------------------------------------------------------------

    def _on_encoder_change(self, value: int):
        pass

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def sub_stabilizer_change(self, listener):
        pass

    def sub_stabilizer_unstable(self, listener):
        pass

    def sub_stabilizer_crash(self, listener):
        pass


class LeftStabilizer(Stabilizer):
    def __init__(self, i2c: I2C):
        super().__init__(i2c, 1, 2, 3, 4)


class RightStabilizer(Stabilizer):
    def __init__(self, i2c: I2C):
        super().__init__(i2c, 17, 18, 19, 20)
