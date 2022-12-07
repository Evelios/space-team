from machine import Pin
from sensor import Switch
import time

led = Pin(25, Pin.OUT)
led.value(1)


def toggle(pin: Pin):
    pin.value(1 - pin.value())


switch = Switch(2, on_change=toggle)

while True:
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
