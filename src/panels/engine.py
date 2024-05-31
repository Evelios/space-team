from machine import I2C

from .fuel_cell import FuelCell


class Engine:
    """
    Engine panel
    """

    def __init__(self, i2c: I2C):
        """
        :param i2c: I2C connection on the board. This allows for connection of the engine to the LCD of the engine.
        """
        self.engine_on_off_pin = 28

        self.fuel_cell1 = FuelCell(on_off_pin=29, cycle_pin=33)
        self.fuel_cell2 = FuelCell(on_off_pin=30, cycle_pin=34)
        self.fuel_cell3 = FuelCell(on_off_pin=31, cycle_pin=35)
        self.fuel_cell4 = FuelCell(on_off_pin=32, cycle_pin=36)

        # Allows for list indexing of fuel cells as well as variable access
        self.fuel_cells = [self.fuel_cell1, self.fuel_cell2, self.fuel_cell3, self.fuel_cell4]

        self.lcd = None
