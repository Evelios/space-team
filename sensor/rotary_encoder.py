from machine import Pin


class RotaryEncoder:
    """
    Mechanical Oak Rotary Encoder

    Encoder has 6 pins and 16 positions all controlled by mechanically rotating
    gears to change the signal. This encoder is going to need some debouncing
    to make sure that the signal doesn't get noisy when sampled.
    """

    def __init__(self, p1, p2, p3, p4, p5, p6):
        """
        Create a rotary encoder from all the 6 pin wired to it.

        :param p1: Pin position 1
        :param p2: Pin position 2
        :param p3: Pin position 3
        :param p4: Pin position 4
        :param p5: Pin position 5
        :param p6: Pin position 6
        """
        self.p1 = Pin(p1, Pin.IN)
        self.p2 = Pin(p2, Pin.IN)
        self.p3 = Pin(p3, Pin.IN)
        self.p4 = Pin(p4, Pin.IN)
        self.p5 = Pin(p5, Pin.IN)
        self.p6 = Pin(p6, Pin.IN)

    def read(self) -> int:
        """
        Get the encoder position
        :return: The current position of the rotary encoder from 0 to 15
        """
        self.p1.value()

        return 0
