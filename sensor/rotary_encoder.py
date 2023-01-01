from machine import Pin


class RotaryEncoder:
    """
    Mechanical Oak Rotary Encoder

    Encoder has 6 pins and 16 positions all controlled by mechanically rotating
    gears to change the signal. This encoder is going to need some debouncing
    to make sure that the signal doesn't get noisy when sampled.
    """
    p1: Pin
    p2: Pin
    p3: Pin
    position: int
    callbacks: list

    def __init__(self, p1, p2, p3, p4):
        """
        Create a rotary encoder from all the 6 pin wired to it.

        :param p1: Pin position 1
        :param p2: Pin position 2
        :param p3: Pin position 3
        :param p4: Pin position 4
        """
        self.p1 = Pin(p1, Pin.IN)
        self.p2 = Pin(p2, Pin.IN)
        self.p3 = Pin(p3, Pin.IN)
        self.p4 = Pin(p4, Pin.IN)
        self.position = 0
        self.callbacks = []

    def read(self) -> int:
        """
        Get the encoder position. The encoder value represents one of the 16
        positions that the rotary encoder can be in. The rotary encoder
        increments when running clockwise. The encoder value is given in
        4 bits from the 4 data input pins on the rotary encoder.

        :return: The current position of the rotary encoder from 0 to 15
        """
        encoding = self.p1.value()
        for pin in [self.p2, self.p3, self.p4]:
            encoding = encoding << 1 + pin.value()

        return encoding

    def update(self):
        reading = self.read()

        if reading != self.position:
            self.position = reading

            for callback in self.callbacks:
                callback()

    # ---- Events ----

    def on_change(self, callback: list) -> None:
        """
        :param callback: Function that gets called when the rotary encoder changes value.
        """
        self.callbacks = self.callbacks + callback
