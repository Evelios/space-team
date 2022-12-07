from machine import Pin
import time


class Button:
    """
    Control buttons that are connected by a single pin. The buttons have
    debouncing built in to avoid noisy inputs when the button is being
    pressed or released.
    """

    HIGH = 1
    LOW = 0
    PRESSED = LOW
    RELEASED = HIGH

    def __init__(self, pin: int, debounce_ms: int = 250):
        """
        Create a button from an input pin.
        :param pin: The digital read pin.
        :param debounce_ms: The number of ms the button
        """
        assert (pin > 0)
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.button_state = self.LOW
        self.last_button_state = self.LOW
        self.debounced = False
        self.debounce_ms = abs(debounce_ms)
        self.last_debounce = time.ticks_ms()

    def update(self) -> None:
        """
        Update the button state with the value on the pin.
        """
        if self.pin.value() == self.LOW:
            self.last_debounce = time.ticks_ms()
            self.button_state = True

        reading = self.pin.value()

        if reading != self.last_button_state:
            self.last_debounce = time.ticks_ms()

        # If the state has lasted for the debounce buffer time and new state is reached
        if time.ticks_diff(time.ticks_ms(), self.last_debounce) > self.debounce_ms and self.button_state != reading:
            self.button_state = reading

        self.last_button_state = reading

    def is_pressed(self) -> bool:
        """
        Check to see if the button is pressed.
        :return: The pressed state of the button
        """
        return self.button_state == self.LOW

    def is_released(self) -> bool:
        """
        Check to see if the button was released.
        :return: True when the button was just released.
        """
        return self.button_state == self.HIGH and self.pin.value() == 0
