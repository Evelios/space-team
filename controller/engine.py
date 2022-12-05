from machine import Pin


class Engine:
    """
    Engine panel
    """

    def __init__(self, cy1, cy2, cy3, cy4):
        """

        :param cy1: Cycle switch 1
        :param cy2: Cycle switch 2
        :param cy3: Cycle switch 3
        :param cy4: Cycle switch 4
        """
        self.cy1 = Pin(cy1, Pin.IN)
        self.cy2 = Pin(cy2, Pin.IN)
        self.cy3 = Pin(cy3, Pin.IN)
        self.cy4 = Pin(cy4, Pin.IN)
