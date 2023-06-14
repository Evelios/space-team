from machine import Pin
from neopixel import NeoPixel


class Heading:
    SIZE = 8
    LEDS = SIZE * SIZE

    def __init__(self, din: int):
        """
        :param din: Data pin for the 8x8 led matrix
        """
        self.din = din
        self.np = NeoPixel(Pin(din), self.LEDS)

    def display(self):
        self.np.fill((255, 0, 0))
