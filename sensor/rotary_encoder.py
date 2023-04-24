from machine import Pin


class RotaryEncoder:
    """
    Mechanical Oak Rotary Encoder

    Encoder has 6 pins and 16 positions all controlled by mechanically rotating
    gears to change the signal. This encoder is going to need some debouncing
    to make sure that the signal doesn't get noisy when sampled.
    """

    def __init__(self, p1, p2, p3, p4):
        """
        Create a rotary encoder from all the 6 pin wired to it.

        :param p1: Pin position 1 (MSB)
        :param p2: Pin position 2
        :param p3: Pin position 3
        :param p4: Pin position 4 (LSB)
        """
        self.p1 = Pin(p1, Pin.IN, Pin.PULL_UP)
        self.p2 = Pin(p2, Pin.IN, Pin.PULL_UP)
        self.p3 = Pin(p3, Pin.IN, Pin.PULL_UP)
        self.p4 = Pin(p4, Pin.IN, Pin.PULL_UP)
        self.v1 = 0
        self.v2 = 0
        self.v3 = 0
        self.v4 = 0
        self.value = 0

    def read(self) -> int:
        """
        Get the encoder position.
        :return: The current position of the rotary encoder from 0 to 15
        """
        self.v1 = 1 - self.p1.value()
        self.v2 = 1 - self.p2.value()
        self.v3 = 1 - self.p3.value()
        self.v4 = 1 - self.p4.value()
        self.value = (self.v1 << 3) + (self.v2 << 2) + (self.v3 << 1) + self.v4

        return self.value
