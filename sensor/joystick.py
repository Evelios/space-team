"""
Original Code by Guy Carver
https://github.com/GuyCarver/MicroPython/blob/master/esp32/joystick.py
"""
from machine import ADC, Pin

class Joystick:
    _x_center = 1789.0
    _y_center = 1817.0
    _pos_x = 4095.0 - _x_center
    _pos_y = 4095.0 - _y_center

    def __init__(self, x_pin, y_pin):
        self._x_axis = ADC(Pin(x_pin))
        self._y_axis = ADC(Pin(y_pin))

        self._x = 0.0
        self._y = 0.0

        self._index = 0
        self._xA = [0, 0, 0]
        self._yA = [0, 0, 0]

    @property
    def x(self):
        """Return value from -1.0 to 1.0."""
        return self._x

    @property
    def y(self):
        """Return value from -1.0 to 1.0."""
        return self._y

    def update(self):
        self._xA[self._index] = self._x_axis.read_u16()
        self._yA[self._index] = self._y_axis.read_u16()

        self._index += 1
        if self._index >= 3:
            self._index = 0

        rx = float(sum(self._xA)) / 3.0 - Joystick._x_center
        ry = float(sum(self._yA)) / 3.0 - Joystick._y_center
        dx = Joystick._pos_x if rx >= 0 else Joystick._x_center
        dy = Joystick._pos_y if ry >= 0 else Joystick._y_center
        self._x = rx / dx
        self._y = ry / dy
