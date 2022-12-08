from machine import Pin
from sensor import Switch, Button, ButtonLed

led = Pin(25, Pin.OUT)
led.off()

print("Space Team!")


def toggle(sw: Switch):
    led.value(sw.value())


def on(button: ButtonLed):
    button.on()


def off(button: ButtonLed):
    button.off()


# switch = Switch(2, on_change=toggle)
click = ButtonLed(3, 4, on_pressed=on, on_released=off)
