from machine import Pin
from sensor import Switch

led = Pin(25, Pin.OUT)

print("Space Team!")


def toggle(sw: Switch):
    led.value(sw.value())


switch = Switch(2, on_change=toggle)
