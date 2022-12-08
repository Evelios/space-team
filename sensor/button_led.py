from machine import Pin

from sensor.button import Button


class ButtonLed(Button):

    def __init__(self, button_pin: int, led_pin: int, *args, **kwargs):
        super().__init__(button_pin, *args, **kwargs)
        self.led = Pin(led_pin, Pin.OUT)
        self.led.off()

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()
