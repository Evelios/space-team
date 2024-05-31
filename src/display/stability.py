import machine
import time
from display.lcd_pico import I2cLcd
from util import clamp, remap


class Stability:
    """
    Stability Panel: Made up of an LCD screen and rotating crank. On the LCD screen you display the stability slider
    and your stability is adjusted with the crank shaft. The crank knows which position it is at by a series of
    mechanical encoders for 24 positions from 4 different pins. Cranking left and right will move stability in the
    same direction if you are looking from the top of the rotation. Clockwise moves right, counterclockwise moves left.
    """
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
        0b11111]

    TOP_INVERTED = [
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b00000]

    TOP_LEFT_ARROW = [
        0b00001,
        0b00001,
        0b00011,
        0b00011,
        0b00111,
        0b00111,
        0b01111,
        0b11000
    ]

    TOP_RIGHT_ARROW = [
        0b10000,
        0b10000,
        0b11000,
        0b11000,
        0b11100,
        0b11100,
        0b11110,
        0b00011]

    BOTTOM = [
        0b11111,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000]

    BOTTOM_INVERTED = [
        0b00000,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111]

    BOTTOM_LEFT_ARROW = [
        0b11000,
        0b01111,
        0b00111,
        0b00111,
        0b00011,
        0b00011,
        0b00001,
        0b00001]

    BOTTOM_RIGHT_ARROW = [
        0b00011,
        0b11110,
        0b11100,
        0b11000,
        0b11000,
        0b11000,
        0b10000,
        0b10000]

    def __init__(self, i2c: machine.I2C, i2c_addr: int):
        self.lcd = I2cLcd(i2c=i2c, i2c_addr=i2c_addr, num_lines=self.ROWS, num_columns=self.COLS)
        time.sleep_ms(100)
        self.__custom_characters()
        self._position = 0

    def __custom_characters(self):
        """ Set the custom characters used for the LCD to display stability. """
        self.top = chr(0)
        self.top_inverted = chr(1)
        self.top_left_arrow = chr(2)
        self.top_right_arrow = chr(3)
        self.bottom = chr(4)
        self.bottom_inverted = chr(5)
        self.bottom_left_arrow = chr(6)
        self.bottom_right_arrow = chr(7)

        self.lcd.custom_char(0, self.TOP)
        self.lcd.custom_char(1, self.TOP_INVERTED)
        self.lcd.custom_char(2, self.TOP_LEFT_ARROW)
        self.lcd.custom_char(3, self.TOP_RIGHT_ARROW)
        self.lcd.custom_char(4, self.BOTTOM)
        self.lcd.custom_char(5, self.BOTTOM_INVERTED)
        self.lcd.custom_char(6, self.BOTTOM_LEFT_ARROW)
        self.lcd.custom_char(7, self.BOTTOM_RIGHT_ARROW)
        self.a = self.position

    @property
    def position(self) -> float:
        """
        Get and set the current stability. The steering is considered stable when at 0. Either direction to -1 or +1 is
        away from the stable point.
        """
        return self._position

    @position.setter
    def position(self, position: float) -> None:
        clamped = clamp(position, -1, 1)
        column = int(round(remap(clamped, -1, 1, 0, self.COLS)))

        if column != self.position:
            self._position = column
            self.display()

    def display(self) -> None:
        self.lcd.clear()
        self.lcd.hide_cursor()

        top = ''
        bottom = ''

        for col in range(self.COLS):
            if col == self.position - 1:
                top += self.top_left_arrow
                bottom += self.bottom_left_arrow
            elif col == self.position:
                top += self.top_inverted
                bottom += self.bottom_inverted
            elif col == self.position + 1:
                top += self.top_right_arrow
                bottom += self.bottom_right_arrow
            else:
                top += self.top
                bottom += self.bottom

        self.lcd.putstr(top)
        self.lcd.putstr(bottom)

    def debug(self):
        self.lcd.clear()
        self.lcd.putstr(f'Stability {self.position}\n')
