from typing import Callable
from pubsub import pub

from hardware.pin_manager import PinManager


def inverse(x):
    """ Get the binary inverse of x. 1 -> 0 and 0 -> 1."""
    return 1 - x


class RotaryEncoder:
    """
    Mechanical Oak Rotary Encoder

    Encoder has 6 pins and 16 positions all controlled by mechanically rotating
    gears to change the signal. This encoder is going to need some debouncing
    to make sure that the signal doesn't get noisy when sampled.
    """
    p1: int
    p2: int
    p3: int
    p4: int
    position: int
    encoded_bits: [int]

    def __init__(self, p1: int, p2: int, p3: int, p4: int):
        """
        Create a rotary encoder from all the 6 pin wired to it.

        :param p1: Pin position 1 (MSB)
        :param p2: Pin position 2
        :param p3: Pin position 3
        :param p4: Pin position 4 (LSB)
        """

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.encoded_bits = [0, 0, 0, 0]
        self.position = 0

        PinManager.sub_digital_change(self.p1, self._on_pin_change)
        PinManager.sub_digital_change(self.p2, self._on_pin_change)
        PinManager.sub_digital_change(self.p3, self._on_pin_change)
        PinManager.sub_digital_change(self.p4, self._on_pin_change)

    def read(self) -> int:
        """
        Get the encoder position. The encoder value represents one of the 16
        positions that the rotary encoder can be in. The rotary encoder
        increments when running clockwise. The encoder value is given in
        4 bits from the 4 data input pins on the rotary encoder.

        :return: The current position of the rotary encoder from 0 to 15
        """
        # TODO: need to fill out immediate read
        return self.position

    # ---- Event Handling ----------------------------------------------------------------------------------------------

    def _on_pin_change(self, pin: int, value: int) -> None:
        # We need to take the inverse of the pin value because 0 indicates an active state
        pin_encoding = inverse(value)
        match pin:
            case self.p1:
                self.encoded_bits[0] = pin_encoding
            case self.p2:
                self.encoded_bits[1] = pin_encoding
            case self.p3:
                self.encoded_bits[2] = pin_encoding
            case self.p4:
                self.encoded_bits[3] = pin_encoding
            case _:
                print(f'RotaryEncoder: Pin change on an invalid pin "{pin}" with value "{value}"')

        # Calculate the new encoder value
        encoder_value = 0
        for pin in self.encoded_bits:
            encoder_value = encoder_value << 1 + pin

        if encoder_value != self.position:
            self.position = encoder_value
            pub.sendMessage(self._change_event_name(), value=self.position)

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def sub_encoder_change(self, listener: Callable[[int], None]) -> None:
        """
        :param listener:
        """
        pub.subscribe(listener, self._change_event_name())

    def _change_event_name(self):
        return f'RotaryEncoder_{self.p1}_{self.p2}_{self.p3}_{self.p4}.ENCODER_CHANGE'
