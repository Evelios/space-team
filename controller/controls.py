from machine import Pin


class Controls:
    """
    Control Panel
    """
    FAN_VENT_NUM = 4
    SWITCH_NUM = 5

    def __init__(self, fv1, fv2, fv3, fv4, sw1, sw2, sw3, sw4, sw5, led4, led5, flush):
        """
        :param fv1: Fan vent pin 1
        :param fv2: Fan vent pin 2
        :param fv3: Fan vent pin 3
        :param fv4: Fan vent pin 4
        :param sw1: Switch pin 1
        :param sw2: Switch pin 2
        :param sw3: Switch pin 3
        :param sw4: Switch pin 4
        :param sw5: Switch pin 5
        :param led4: Switch 4 led pin
        :param led5: Switch 5 led pin
        :param flush: Flush switch pin
        """

        self.fv1 = Pin(fv1, Pin.IN)
        self.fv2 = Pin(fv2, Pin.IN)
        self.fv3 = Pin(fv3, Pin.IN)
        self.fv4 = Pin(fv4, Pin.IN)
        self.sw1 = Pin(sw1, Pin.IN)
        self.sw2 = Pin(sw2, Pin.IN)
        self.sw3 = Pin(sw3, Pin.IN)
        self.sw4 = Pin(sw4, Pin.IN)
        self.sw5 = Pin(sw5, Pin.IN)
        self.led4 = Pin(led4, Pin.IN)
        self.led5 = Pin(led5, Pin.IN)
        self.flush = Pin(flush, Pin.IN)

    def read_fan_vent(self, vent_id: int = 0):
        assert (0 <= vent_id < 4)
