from machine import I2C
import utime
from pico_i2c_lcd import I2cLcd


class HorizontalDial:
    ROWS = 2
    COLS = 16

    TOP = [
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b11111
    ]

    TOP_INDICATOR = [
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00100,
        0b01110,
        0b11111]

    BOTTOM = [
        0b11111,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000
    ]

    BOTTOM_INDICATOR = [
        0b11111,
        0b01110,
        0b00100,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000]

    def __init__(self, i2c: I2C, i2c_addr: int = 39):
        self.lcd = I2cLcd(i2c=i2c, i2c_addr=i2c_addr, num_lines=self.ROWS, num_columns=self.COLS)
        utime.sleep_ms(100)
        self.__custom_characters()

    def __custom_characters(self):
        self.lcd.custom_char(0, self.TOP)
        self.lcd.custom_char(1, self.TOP_INDICATOR)
        self.lcd.custom_char(2, self.BOTTOM)
        self.lcd.custom_char(3, self.BOTTOM_INDICATOR)

    def display(self):
        self.lcd.clear()
        self.lcd.hide_cursor()

        top = ""
        bottom = ""
        for col in range(self.COLS):
            if (col - self.COLS) % 2 == 1:
                top += chr(0)
                bottom += chr(2)
            else:
                top += chr(1)
                bottom += chr(3)

        self.lcd.putstr(top)
        self.lcd.putstr(bottom)
