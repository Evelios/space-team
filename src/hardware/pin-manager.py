from .adcmux import AdcMux

from mcp2317 import *
from i2c import I2C
import smbus


class SpaceTeam:

    def __init__(self, i2c: I2C):
        self.i2c = i2c
        self.pins1to16 = MCP23017(0x20, i2c)
        self.pins17to32 = MCP23017(0x21, i2c)
        self.pins33to48 = MCP23017(0x22, i2c)
        self.adc = AdcMux(1, 0, 0, 0, 0)

    # Set the pin mode of a pin on the chip
    def set_pin_mode(self, pin: int, mode: int) -> None:
        if pin < 0:
            return
        elif pin <= 16:
            self.pins1to16.set_pin_mode(pin, mode)
        elif pin <= 32:
            self.pins17to32.set_pin_mode(pin - 16, mode)
        elif pin <= 48:
            self.pins33to48.set_pin_mode(pin - 32, mode)
        elif pin <= 64:
            # TODO: allow for modification of local DIO
            return
        else:
            return

    def digital_write(self, pin: int, value: int) -> None:
        if pin < 0:
            return
        elif pin <= 16:
            self.pins1to16.digital_write(pin, value)
        elif pin <= 32:
            self.pins17to32.digital_write(pin - 16, value)
        elif pin <= 48:
            self.pins33to48.digital_write(pin - 32, value)
        elif pin <= 64:
            # TODO: allow for modification of local DIO
            return
        else:
            return

    def digital_read(self, pin: int) -> int:
        if pin < 0:
            return 0
        elif pin <= 16:
            self.pins1to16.digital_read(pin)
        elif pin <= 32:
            self.pins17to32.digital_read(pin - 16)
        elif pin <= 48:
            self.pins33to48.digital_read(pin - 32)
        elif pin <= 64:
            # TODO: allow for modification of local DIO
            return 0
        else:
            return 0

    def analog_read(self, pin: int) -> int:
        return self.adc.read(pin)

    def analog_write(self, pin:int, value:int) -> None:
