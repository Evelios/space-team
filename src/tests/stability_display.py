# I2C Connected to LCD display with 5v from USB. There are two 5k resistors pulling up the SCL(1) and SDA(0) pins.

from machine import Pin, I2C
import time

from display.stability import Stability


def main():
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

    time.sleep_ms(100)

    devices = i2c.scan()

    if len(devices) == 0:
        print("No i2c device !")
        return
    else:
        print('i2c devices found:', len(devices))

    for device in devices:
        print("Decimal address: ", device, " | Hexa address: ", hex(device))

    stability = Stability(i2c, i2c_addr=devices[0])
    stability.position = 0

    direction = 1
    for i in range(0, 50):
        # Switch directions when the position gets to the ends
        if stability.position == direction:
            direction = direction * -1

        stability.position = direction * 0.1
        stability.display()
        time.sleep_ms(250)
