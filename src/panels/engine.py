from machine import Pin


class Engine:
    """
    Engine panel
    """

    def __init__(self, pinmanager, i2c):
        """
        :param pinmanager:
        :param i2c:
        """
        self.cycle1 = 1
        self.cycle2 = 2
        self.cycle3 = 3
        self.cycle4 = 4

        self.fuel_cell1 = 5
        self.fuel_cell2 = 6
        self.fuel_cell3 = 7
        self.fuel_cell4 = 8

        self.on_off = 9

        self.lcd = None
