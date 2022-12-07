from machine import Pin


class Switch:
    """
    Class to control an external switch.
    """

    def __init__(self, pin: int, pull=Pin.PULL_UP, on_change=None):
        """
        :param pin: The pin the switch is attached to.
        :param pull:
            The pull mode for the switch. The default is PULL_UP. This lets
            you only need ground reference when hooking up switches.

            PULL_UP - Switches are grounded when switch is active
            PULL_DOWN - Switches are connected to Vcc when switch is active
        :param on_change:
            Callback function for when a switch value changes.
            The callback function takes only one argument, the switch that changed.
        """
        self.pin = Pin(pin, mode=Pin.IN, pull=pull)
        self.on_change = on_change
        self.pull = pull

        # Set pin interrupt handlers
        self.pin.irq(handler=self.callback, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

    def callback(self, _: Pin):
        if self.on_change is not None:
            self.on_change(self)

    def value(self) -> int:
        """
        :return: 1 if the switch is active and 0 if the switch is inactive.
        """
        if self.pull == Pin.PULL_DOWN:
            return self.pin.value()
        else:
            # Invert the value when using PULL_UP mode
            return 1 - self.pin.value()
