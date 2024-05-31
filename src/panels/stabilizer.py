from enum import Enum, auto
from machine import I2C
from pubsub import pub
from typing import Callable

from sensor.rotary_encoder import RotaryEncoder


class Stabilizer:
    """
    Stabilizer panel
    """

    class Event(Enum):
        POSITION_CHANGE = auto()
        UNSTABLE = auto()
        CRASH = auto()

    stability: float = 0
    """Stability of this device. Range -1 -> 1"""

    rotary_encoder: RotaryEncoder
    """stabilizer_input"""

    previous_reading: float = 0

    def __init__(self, i2c: I2C, p1: int, p2: int, p3: int, p4: int):
        self.i2c = i2c
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.rotary_encoder = RotaryEncoder(p1, p2, p3, p4)

    def update(self):
        encoder_reading = self.rotary_encoder.read()

        if encoder_reading == self.previous_reading:
            return

        self.stability += self.previous_reading - encoder_reading
        self.previous_reading = encoder_reading

    # ---- Event Handling ----------------------------------------------------------------------------------------------

    def _on_encoder_change(self, value: int):
        pass

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def sub_stabilizer_change(self, listener: Callable[[float], None]) -> None:
        """
        Subscribe to the stabilizer value changing.

        :param listener: Callback function taking the following arguments.
            - `value` (`float`): Current stabilizer value
        """
        event_name = self._event_name(Stabilizer.Event.POSITION_CHANGE, self.p1)
        pub.subscribe(listener, event_name)

    def unsub_stabilizer_change(self, listener: Callable[[float], None]) -> None:
        """
        Unsubscribe to the stabilizer value changing.

        :param listener: Callback function taking the following arguments.
            - `value` (`float`): Current stabilizer value
        """
        event_name = self._event_name(Stabilizer.Event.POSITION_CHANGE, self.p1)
        pub.unsubscribe(listener, event_name)

    def sub_stabilizer_unstable(self, listener) -> None:
        """
        Subscribe to the stabilizer becoming unstable.

        :param listener: Callback function taking the following arguments.
            - `value` (`float`): Current stabilizer value
        """
        event_name = self._event_name(Stabilizer.Event.UNSTABLE, self.p1)
        pub.subscribe(listener, event_name)

    def unsub_stabilizer_unstable(self, listener) -> None:
        """
        Unsubscribe to the stabilizer becoming unstable.

        :param listener: Callback function taking the following arguments.
            - `value` (`float`): Current stabilizer value
        """
        event_name = self._event_name(Stabilizer.Event.UNSTABLE, self.p1)
        pub.unsubscribe(listener, event_name)

    def sub_stabilizer_crash(self, listener):
        """
        Subscribe to the stabilizer crashing into the edge of the limit.

        :param listener: Callback function taking the following arguments.
            - `value` (`float`): Current stabilizer value
        """
        event_name = self._event_name(Stabilizer.Event.CRASH, self.p1)
        pub.subscribe(listener, event_name)

    def unsub_stabilizer_crash(self, listener):
        """
        Unsubscribe to the stabilizer crashing into the edge of the limit.

        :param listener: Callback function taking the following arguments.
            - `value` (`float`): Current stabilizer value
        """
        event_name = self._event_name(Stabilizer.Event.CRASH, self.p1)
        pub.unsubscribe(listener, event_name)

    @staticmethod
    def _event_name(event: Event, pin: int):
        return f'{event}_{pin}'


class LeftStabilizer(Stabilizer):
    def __init__(self, i2c: I2C):
        super().__init__(i2c, 1, 2, 3, 4)


class RightStabilizer(Stabilizer):
    def __init__(self, i2c: I2C):
        super().__init__(i2c, 17, 18, 19, 20)
