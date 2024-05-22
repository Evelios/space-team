from machine import Pin, I2C
from hardware.pin_manager import PinManager

# from display.pico_i2c_lcd import I2cLcd
from sensor.rotary_encoder import RotaryEncoder


class Stabilizer:
    """
    Stabilizer panel
    """

    stability = 0
    """Stability of this device. Range -1 -> 1"""

    rotary_encoder = RotaryEncoder
    """stabilizer_input"""
    previous_reading = 0

    def __init__(self, pin_manager: PinManager, i2c: I2C, p1: int, p2: int, p3: int, p4: int):
        self.pin_manager = pin_manager
        self.i2c = i2c
        self.rotary_encoder = RotaryEncoder(p1, p2, p3, p4)

    def update(self):
        encoder_reading = self.rotary_encoder.read()

        if encoder_reading == self.previous_reading:
            return

        self.stability += self.previous_reading - encoder_reading
        self.previous_reading = encoder_reading
