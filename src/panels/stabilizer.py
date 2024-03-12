from machine import Pin, I2C

from display.pico_i2c_lcd import I2cLcd
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

    def __init__(self, p1, p2, p3, p4):
        self.rotary_encoder = RotaryEncoder(p1, p2, p3, p4)

        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
        self.lcd = I2cLcd(i2c=i2c, i2c_addr=0x3f, num_lines=2, num_columns=16)

    def update(self):
        encoder_reading = self.rotary_encoder.read()

        if encoder_reading == self.previous_reading:
            return

        self.lcd.move_to(0, 0)
        self.lcd.putstr("     ")
        self.lcd.move_to(0, 0)
        # self.lcd.putstr(f"{encoder_reading} : {self.stability}")
        self.lcd.move_to(0, 1)
        # self.lcd.putstr(f"{self.rotary_encoder.v1} {self.rotary_encoder.v2} {self.rotary_encoder.v3} {self.rotary_encoder.v4}")

        self.stability += self.previous_reading - encoder_reading
        self.previous_reading = encoder_reading

