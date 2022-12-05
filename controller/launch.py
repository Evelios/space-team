from machine import Pin


class Launch:
    """
    Launch panel
    """

    def __init__(self, key, start, estop, mileage):
        """
        :param key: Key pin
        :param start: Start button pin
        :param estop: Emergency stop pin
        :param mileage: Mileage pin
        """

        self.key = Pin(key, Pin.IN)
        self.start = Pin(start, Pin.IN)
        self.estop = Pin(estop, Pin.IN)
        self.mileage = Pin(mileage, Pin.IN)