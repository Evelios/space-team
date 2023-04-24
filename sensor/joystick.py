"""
Original Code by Guy Carver
https://github.com/GuyCarver/MicroPython/blob/master/esp32/joystick.py
"""
from machine import ADC, Pin


class Joystick:
    _x_center = 31500.
    _x_min = 6750.
    _x_max = 57500.
    _pos_x = 65535. - _x_center

    _y_center = 33000.
    _y_min = 6500.
    _y_max = 60000.
    _pos_y = 65535. - _y_center

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
        x = self._x_axis.read_u16()
        y = self._y_axis.read_u16()

        self._x_min = min(self._x_min, x)
        self._y_min = min(self._y_min, y)
        self._x_max = min(self._x_max, x)
        self._y_max = min(self._y_max, y)

        self._xA[self._index] = x
        self._yA[self._index] = y

        self._index += 1
        if self._index >= 3:
            self._index = 0

        rx = float(sum(self._xA)) / 3.0 - Joystick._x_center
        ry = float(sum(self._yA)) / 3.0 - Joystick._y_center
        dx = Joystick._pos_x if rx >= 0 else Joystick._x_center
        dy = Joystick._pos_y if ry >= 0 else Joystick._y_center
        self._x = rx / dx
        self._y = ry / dy
