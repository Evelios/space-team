from typing import Union, Callable
import machine
from pubsub.publisher import Publisher

from .mcp23017 import MCP23017
from .adcmux import AdcMux


class PinManager:
    """
    The PinManager is responsible for accessing, updating, and handing out pins on the shuttle control module. The pin
    manager takes care of routing communication through the digital and analog input/output expander chips.
    """

    class Event:
        DIGITAL_RISING = 'PinManager.DigitalRising'
        DIGITAL_FALLING = 'PinManager.DigitalFalling'
        DIGITAL_CHANGE = 'PinManager.DigitalChange'
        ANALOG_CHANGE = 'PinManager.AnalogChange'

    def __init__(self, i2c: machine.I2C):
        self.publisher = Publisher()

        self.i2c = i2c

        self.pins1to16 = MCP23017(i2c, 0x20)
        self.pins17to32 = MCP23017(i2c, 0x21)
        self.pins49to64 = MCP23017(i2c, 0x22)
        self.adc = AdcMux(1, 0, 0, 0, 0)
        self.local_pins: dict[int, Union[machine.Pin, machine.ADC]] = {}  # Holds the gpio 33 -> 48

        # Sampling for reading pin inputs and monitoring for changes
        self._sample_rate = 50  # ms
        self.sample_timer = machine.Timer(period=self._sample_rate, callback=self._sample_pins)

        # Initialize a dictionary of previous digital and analog pin states
        self.digital_pins = {key: 0 for key in range(1, 65)}
        self.analog_pins = {key: 0.0 for key in range(1, 17)}

    # ---- Private Methods ---------------------------------------------------------------------------------------------
    def _init_local_io(self):
        for gpio in range(33, 42 + 1):
            pin = gpio - 27  # Pin offset for the first section of IO pins
            self.local_pins[gpio] = machine.Pin(pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

        for gpio in range(43, 47):
            pin = 64 - gpio  # Pin offset for the second section of IO pins
            self.local_pins[gpio] = machine.Pin(pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

        a1 = machine.ADC(1)
        a2 = machine.ADC(2)

        self.local_pins[47] = a1
        self.local_pins[48] = a2

    # ---- Digital Pin Logic -------------------------------------------------------------------------------------------

    def set_pin_mode(self, gpio: int, mode: int) -> None:
        """
        Set the pin mode of a pin on the chip

        :param gpio: Pin number for GPIO 1 -> 64
        :param mode: 1 = input pin, 0 = output pin
        """
        if gpio <= 0:
            return

        elif gpio <= 16:
            pin = gpio - 1
            self.pins1to16.pin(pin, mode)

        elif gpio <= 32:
            pin = gpio - 17
            self.pins17to32.pin(pin, mode)

        # Local Pins
        elif gpio <= 46:
            if mode == 1:
                pin_mode = machine.Pin.IN
            elif mode == 0:
                pin_mode = machine.Pin.OUT
            else:
                return

            self.local_pins[gpio].mode(pin_mode)

        # Don't need to handle setting the mode for the ADC Pins
        elif gpio == 47 or gpio == 48:
            return

        elif gpio < 64:
            pin = gpio - 49
            self.pins49to64.pin(pin, mode)

        else:
            return

    def digital_write(self, gpio: int, value: int) -> None:
        """
        Write to a digital GPIO pin.
        :param gpio:
        :param value:
        """
        if gpio < 0:
            return

        elif gpio <= 16:
            pin = gpio - 1
            self.pins1to16[pin].value(value)

        elif gpio <= 32:
            pin = gpio - 17
            self.pins17to32[pin].value(value)

        elif gpio <= 46:
            self.local_pins[gpio].value(value)

        # Cannot write to the two analog pins
        elif gpio <= 48:
            return

        elif gpio <= 64:
            pin = gpio - 49
            self.pins49to64[pin].value(value)

        else:
            return

    def digital_read(self, gpio: int) -> int:
        """
        Read a digital pin and return the value at that gpio output. This gets the current value from the pin and
        doesn't run any internal logic to detect pin state changes, nor does it fire off events.

        :param gpio: The GPIO pin from the module
        :return: The pin value 0 - Low, 1 - High
        """
        if gpio <= 0:
            return 0

        elif gpio <= 16:
            pin = gpio - 1
            return self.pins1to16[pin].value()

        elif gpio <= 32:
            pin = gpio - 17
            return self.pins17to32[pin].value()

        elif gpio <= 46:
            return self.local_pins[gpio].value()

        # Analog pins don't have a digital read value
        elif gpio <= 48:
            return 0

        elif gpio <= 64:
            pin = gpio - 48
            return self.pins49to64[pin].value()

        else:
            return 0

    # ---- Analog Pin Logic --------------------------------------------------------------------------------------------

    def analog_read(self, gpio: int) -> int:
        """
        Read the analog value from the

        :param gpio: The GPIO pin location of the analog read pins
        :return: Analog value from the ADC as an unsigned 16-bit integer
        """
        if gpio in (47, 48):
            self.local_pins[gpio].read_u16()

        if gpio in range(1, 17):
            return self.adc.read(gpio)

        return 0

    # ---- Event Handling Logic ----------------------------------------------------------------------------------------

    def _sample_pins(self):
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

                # Send the message for either the Digital Rising or Falling event
                if new_value == 0:
                    self.publisher.send_message(
                        self._pin_event_name(PinManager.Event.DIGITAL_RISING, pin),
                        pin=pin, value=new_value)

                    self.publisher.send_message(
                        self._pin_event_name(PinManager.Event.DIGITAL_CHANGE, pin),
                        pin=pin, value=new_value)
                else:
                    self.publisher.send_message(
                        self._pin_event_name(PinManager.Event.DIGITAL_FALLING, pin),
                        pin=pin, value=new_value)

                    self.publisher.send_message(
                        self._pin_event_name(PinManager.Event.DIGITAL_CHANGE, pin),
                        pin=pin, value=new_value)

    def _sample_analog_pins(self):
        for pin in range(1, 17):
            new_value = self.analog_read(pin)

            # Make sure to create a value in the digital read table if no reading currently exists
            if pin not in self.analog_pins:
                self.analog_pins[pin] = new_value

            # If a new value is read, update the current value stored and run any stored callbacks
            elif new_value != self.analog_pins[pin]:
                self.analog_pins[pin] = new_value
                self.publisher.send_message(self._pin_event_name(PinManager.Event.ANALOG_CHANGE, pin), pin=pin,
                                            value=new_value)

    def sub_digital_rising(self, pin: int, listener: Callable) -> None:
        """
        Attach a callback to the digital pin. When a state changes to high, run the stored callbacks for that pin.
        """
        self.publisher.subscribe(PinManager._pin_event_name(PinManager.Event.DIGITAL_RISING, pin), listener)

    def sub_digital_falling(self, pin: int, listener: Callable) -> None:
        """
        Attach a callback to the pin manager. When a state change to low, run the stored callbacks for that
        pin.
        """
        self.publisher.subscribe(PinManager._pin_event_name(PinManager.Event.DIGITAL_FALLING, pin), listener)

    def sub_digital_change(self, pin: int, listener: Callable) -> None:
        """
        Attach a callback to the pin manager. When a state change occurs on any pin, run the stored callbacks for that
        pin.
        """
        self.publisher.subscribe(PinManager._pin_event_name(PinManager.Event.DIGITAL_CHANGE, pin), listener)

    def sub_analog_change(self, pin: int, listener: Callable) -> None:
        """
        Attach a callback to the analog pin. When a state change occurs on any digital pin, run the stored callbacks for
        that pin.
        """
        self.publisher.subscribe(PinManager._pin_event_name(PinManager.Event.ANALOG_CHANGE, pin), listener)

    @staticmethod
    def _pin_event_name(event: str, pin: int) -> str:
        """
        Get the string representation of the event on a particular pin. The event name is needed as a string for the\
        PyPubSub class which handles the observer pattern for the PinManager.
        """
        return f"{event}_{pin}"
