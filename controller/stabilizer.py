from machine import Pin, I2C

from util import clamp

from display import Stability
from sensor import RotaryEncoder


class Stabilizer:
    """
    Stabilizer panel
    """
    stability = 0
    """Stability of this device. Range -1 -> 1"""

    rotary_encoder: RotaryEncoder = None
    """stabilizer_input"""

    stability_display: Stability = None
    """LCD panel screen for the stabilizer display"""

    def __init__(self, p1: Pin, p2: Pin, p3: Pin, p4: Pin, i2c: I2C):
        """

        :param p1: Pin 1, MSB of the rotary encoder
        :param p2: Pin 2
        :param p3: Pin 3
        :param p4: Pin 4, LSB of the rotary encoder

        """
        self.rotary_encoder = RotaryEncoder(p1, p2, p3, p4)
        self.stability_display = Stability(i2c)

    def on_crank(self) -> None:
        """
        The action taken when the stabilizer wheel is changed.

        """
        self.stability = clamp(self.stability + 0.1, -1, 1)
        self.stability_display.set_position(self.stability)
