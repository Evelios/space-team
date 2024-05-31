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

    def __init__(self, pin: int, debounce_ms: int = 250, on_pressed=None, on_released=None):
        """
        Create a button from an input pin.
        :param pin: The digital read pin.
        :param debounce_ms: The number of ms the button
        :param on_pressed:
            Callback for when a button is pressed.
            It must take this button object as it's only parameter.
        :param on_released:
            Callback for when a button is released
            It must take this button object as it's only parameter.
        """
        assert (pin > 0)
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.button_state = self.LOW
        self.last_button_state = self.LOW
        self.debounced = False
        self.debounce_ms = abs(debounce_ms)
        self.last_debounce = time.ticks_ms()
        self.on_pressed = on_pressed
        self.on_released = on_released

        self.pin.irq(handler=self.on_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

    def on_change(self, _: Pin):
        """
        Update the button state with the value on the pin.
        :param _: Pin that is being changed. This is the same as `self.pin` so we are ignoring the input value
        """
        reading = self.pin.value()

        if reading == self.PRESSED and self.on_pressed is not None:
            self.on_pressed(self)
        elif reading == self.RELEASED and self.on_released is not None:
            self.on_released(self)

        self.button_state = reading

        # if self.pin.value() == self.LOW:
        #     self.last_debounce = time.ticks_ms()
        #     self.button_state = True
        #
        # reading = self.pin.value()
        #
        # if reading != self.last_button_state:
        #     self.last_debounce = time.ticks_ms()
        #
        # # If the state has lasted for the debounce buffer time and new state is reached
        # if time.ticks_diff(time.ticks_ms(), self.last_debounce) > self.debounce_ms and self.button_state != reading:
        #     self.button_state = reading
        #
        #     # Run callback functions if present
        #     if reading == self.PRESSED and self.on_pressed is not None:
        #         self.on_pressed(self)
        #     elif reading == self.RELEASED and self.on_released is not None:
        #         self.on_released(self)
        #
        # self.last_button_state = reading

    def is_pressed(self) -> bool:
        """
        Check to see if the button is pressed.
        :return: The pressed state of the button
        """
        return self.button_state == self.PRESSED

    def is_released(self) -> bool:
        """
        Check to see if the button was released.
        :return: True when the button was just released.
        """
        return self.button_state == self.RELEASED and self.pin.value() == 0
