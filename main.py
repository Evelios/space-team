import utime

import machine
from machine import I2C
from pico_i2c_lcd import I2cLcd

from horizontal import HorizontalDial

I2C_ADDR = 39

print("Running test_main")

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
dial = HorizontalDial(i2c, I2C_ADDR)


dial.display()
