from machine import Pin

class Mileage:
    pin: Pin

    def __init__(self, pin: int):
        self.pin = Pin(pin, Pin.OUT)

    def increment(self) -> None:
        self.pin.high()
        self.pin.low()
