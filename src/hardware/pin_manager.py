

from mcp2317 import MCP23017
from i2c import I2C
import machine
import smbus

from .adcmux import AdcMux
from util import clamp


class PinManager:
    """
    The PinManager is responsible for accessing, updating, and handing out pins on the shuttle control module. The pin
    manager takes care of routing communication through the digital and analog input/output expander chips.
    """

    def __init__(self, i2c: I2C):
        self.i2c = i2c

        self.pins1to16 = MCP23017(0x20, i2c)
        self.pins17to32 = MCP23017(0x21, i2c)
        self.pins33to48 = MCP23017(0x22, i2c)
        self.adc = AdcMux(1, 0, 0, 0, 0)

        # Sampling for reading pin inputs and monitoring for changes
        self._sample_rate = 50  # ms
        self.sample_timer = machine.Timer(period=self._sample_rate, callback=self.sample_pins)

        # Initialize a dictionary of previous digital pin states
        self.digital_pins = {(key, 0) for key in range(1, 65)}
        self.digital_callbacks = {}
        self.digital_callbacks_any_pin = []

        # Initialize a dictionary of previous analog pin states
        self.analog_pins = {(key, 0.0) for key in range(1, 17)}
        self.analog_callbacks = {}
        self.analog_callbacks_any_pin = []

    # ---- Digital Pin Logic -------------------------------------------------------------------------------------------

    # Set the pin mode of a pin on the chip
    def set_pin_mode(self, pin: int, mode: int) -> None:
        if pin < 0:
            return
        elif pin <= 16:
            self.pins1to16.set_pin_mode(pin, mode)
        elif pin <= 32:
            self.pins17to32.set_pin_mode(pin - 16, mode)
        elif pin <= 48:
            return
            # TODO: allow for modification of local DIO
        elif pin <= 64:
            self.pins33to48.set_pin_mode(pin - 48, mode)
        else:
            return

    def digital_write(self, pin: int, value: int) -> None:
        if pin < 0:
            return
        elif pin <= 16:
            self.pins1to16.digital_write(pin, value)
        elif pin <= 32:
            self.pins17to32.digital_write(pin - 16, value)
        elif pin <= 48:
            return
            # TODO: allow for modification of local DIO
        elif pin <= 64:
            self.pins33to48.digital_write(pin - 48, value)
        else:
            return

    def digital_read(self, pin: int) -> int:
        if pin < 0:
            return 0
        elif pin <= 16:
            self.pins1to16.digital_read(pin)
        elif pin <= 32:
            self.pins17to32.digital_read(pin - 16)
        elif pin <= 48:
            return 0
            # TODO: allow for modification of local DIO
        elif pin <= 64:
            self.pins33to48.digital_read(pin - 48)
        else:
            return 0

    # ---- Analog Pin Logic --------------------------------------------------------------------------------------------

    def analog_read(self, pin: int) -> int:
        if pin in (47, 48):
            # TODO: Handle reading internal ADC Pins
            return 0

        return self.adc.read(pin)

    def analog_write(self, pin: int, value: int) -> None:
        if pin in (47, 48):
            # TODO: Handle writing internal ADC Pins
            return

        self.adc.write(pin, value)

    # ---- Event Handling Logic ----------------------------------------------------------------------------------------

    def sample_pins(self):
        """
        Sample the digital and analog pins. This pin sampling will happen on a periodic cycle. If any pins have state
        changes, all callbacks associated with a pin will be called.
        """
        self._sample_digital_pins()
        self._sample_analog_pins()

    def _sample_digital_pins(self):
        for pin in range(1, 65):
            new_value = self.digital_read(pin)

            # Make sure to create a value in the digital read table if no reading currently exists
            if pin not in self.digital_pins:
                self.digital_pins[pin] = new_value

            # If a new value is read, update the current value stored and run any stored callbacks
            elif new_value != self.digital_pins[pin]:
                self.digital_pins[pin] = new_value

                # Run all callback functions on pin changes
                if pin in self.digital_callbacks:
                    for callback in self.digital_callbacks[pin]:
                        callback(new_value)

                    for callback in self.digital_callbacks_any_pin:
                        callback(pin, new_value)

    def _sample_analog_pins(self):
        for pin in range(1, 17):
            new_value = self.analog_read(pin)

            # Make sure to create a value in the digital read table if no reading currently exists
            if pin not in self.analog_pins:
                self.analog_pins[pin] = new_value

            # If a new value is read, update the current value stored and run any stored callbacks
            elif new_value != self.analog_pins[pin]:
                self.analog_pins[pin] = new_value

                # Run all callback functions on pin changes
                if pin in self.analog_callbacks:
                    for callback in self.analog_callbacks[pin]:
                        callback(new_value)

                    for callback in self.analog_callbacks_any_pin:
                        callback(pin, new_value)

    def on_digital_change(self, pin: int, callback):
        """
        Attach a callback to the digital pin. When a state change occurs, run the stored callbacks for that pin.
        """
        if pin not in self.digital_callbacks:
            self.digital_callbacks[pin] = []

        self.digital_callbacks[pin].append(callback)

    def on_any_digital_change(self, callback):
        """
        Attach a callback to the pin manager. When a state change occurs on any pin, run the stored callbacks for that
        pin.
        """
        self.digital_callbacks_any_pin.append(callback)

    def on_analog_change(self, pin: int, callback):
        """
        Attach a callback to the analog pin. When a state change occurs on any digital pin, run the stored callbacks for
        that pin.
        """
        if pin not in self.analog_callbacks:
            self.analog_callbacks[pin] = []

        self.analog_callbacks[pin].append(callback)

    def on_any_analog_change(self, callback):
        """
        Attach a callback to the pin manager. When a state change occurs on any analog pin, run the stored callbacks for
        that pin.
        """
        self.analog_callbacks_any_pin.append(callback)
