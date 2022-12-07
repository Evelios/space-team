from machine import Pin


class Switch:
    """
    Class to control an external switch.
    """

    def __init__(self, pin: int, pull=Pin.PULL_UP):
        """
        :param pin: The pin the switch is attached to.
        :param pull:
            The pull mode for the switch. The default is PULL_UP.
            PULL_UP - Switches are grounded when switch is active
            PULL_DOWN - Switches are connected to Vcc when switch is active
        """
        self.pin = Pin(pin, mode=Pin.IN, pull=pull)
        self.state = self.pin.value()

        # Set pin interrupt handlers
        Pin.irq(handler=self.on_activate(), trigger=Pin.Pin.IRQ_RISING)
        Pin.irq(handler=self.on_deactivate(), trigger=Pin.IRQ_FALLING)

    def on_activate(self, pin: Pin):

        self.state = 1

    def on_deactivate(self, pin: Pin):
        self.state = 0
