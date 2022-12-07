from machine import Pin
from sensor import Switch


class Controls:
    """
    Control Panel
    """
    FAN_VENT_NUM = 4
    SWITCH_NUM = 5

    def __init__(self, fv1: int, fv2: int, fv3: int, fv4: int,
                 sw1: int, sw2: int, sw3: int, sw4: int, sw5: int,
                 led4: int, led5: int, flush: int):
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

        self.fv1 = Switch(fv1)
        self.fv2 = Switch(fv2)
        self.fv3 = Switch(fv3)
        self.fv4 = Switch(fv4)

        self.fan_vents = [self.fv1, self.fv2, self.fv3, self.fv4]

        self.sw1 = Pin(sw1, Pin.IN)
        self.sw2 = Pin(sw2, Pin.IN)
        self.sw3 = Pin(sw3, Pin.IN)
        self.sw4 = Pin(sw4, Pin.IN)
        self.sw5 = Pin(sw5, Pin.IN)
        self.led4 = Pin(led4, Pin.IN)
        self.led5 = Pin(led5, Pin.IN)

        self.clackies = [self.sw1, self.sw2, self.sw3, self.sw4, self.sw5]

        self.flush = Pin(flush, Pin.IN)


def read_fan_vent(self, vent_id: int = 0):
    assert (0 <= vent_id < 4)
    match vent_id:
        case 0:
            self.fv1.state
        case 1:
            self.fv2.state
        case 2:
            self.fv3.state
        case 3:
            self.fv4.state
