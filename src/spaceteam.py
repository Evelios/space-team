from mcp2317 import *
from i2c import I2C
import smbus

class SpaceTeam:

    def __init__(self):
        self.i2c = I2C(smbus.SMBUS(1))
