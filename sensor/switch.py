from machine import Pin


class Switch:
    """
    Class to control an external switch.
    """

    def __init__(self, pin: int, pull=Pin.PULL_UP, on_change=None):
        """
        :param pin: The pin the switch is attached to.
        :param pull:
            The pull mode for the switch. The default is PULL_UP.
            PULL_UP - Switches are grounded when switch is active
            PULL_DOWN - Switches are connected to Vcc when switch is active
        :param on_change:
            Callback function for when a switch value changes.
            The callback function takes only one argument, the switch that changed.
        """
        self.pin = Pin(pin, mode=Pin.IN, pull=pull)
        self.state = self.pin.value()
        self.on_change = on_change

        # Set pin interrupt handlers
        self.pin.irq(handler=self.on_activate, trigger=Pin.IRQ_RISING)
        self.pin.irq(handler=self.on_deactivate, trigger=Pin.IRQ_FALLING)

    def on_activate(self, _: Pin):
        if self.on_change is not None:
            self.on_change(self)
        self.state = 1

    def on_deactivate(self, _: Pin):
        if self.on_change is not None:
            self.on_change(self)
        self.state = 0
