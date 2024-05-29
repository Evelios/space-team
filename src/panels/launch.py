from enum import Enum, auto
from pubsub import pub
from typing import Callable

from hardware.pin_manager import PinManager
from hardware import states


class Launch:
    """
    Launch panel
    """

    class Event(Enum):
        KEY_TOGGLE = auto()
        ESTOP_TOGGLE = auto()
        START_BUTTON_PRESSED = auto()
        DIFFICULTY_CHANGED = auto()

    def __init__(self):
        self.key_pin = 40
        self.start_pin = 38
        self.estop_pin = 39
        self.mileage_pin = 37

        self.difficulty_pins = list(range(41, 47))

        PinManager.sub_digital_change(self.key_pin, self._on_key_toggle)
        PinManager.sub_digital_change(self.estop_pin, self._on_estop_toggle)
        PinManager.sub_digital_falling(self.start_pin, self._on_start_button_pressed)

    # ---- Properties ------------------------------------------------------------------------------------------------

    # ---- Modifiers ---------------------------------------------------------------------------------------------------

    def increase_mileage(self) -> None:
        pass

    # ---- Event Handling ----------------------------------------------------------------------------------------------

    @staticmethod
    def _on_key_toggle(value: int):
        # The key is N/O and pulled high when open, the pin is active low
        switch_state = states.Switch.ON if value == 0 else states.Switch.OFF
        pub.sendMessage(str(Launch.Event.KEY_TOGGLE), state=switch_state)

    @staticmethod
    def _on_estop_toggle(value: int):
        # The key is N/O and pulled high when open, the pin is active low
        switch_state = states.Switch.ON if value == 0 else states.Switch.OFF
        pub.sendMessage(str(Launch.Event.ESTOP_TOGGLE), state=switch_state)

    @staticmethod
    def _on_start_button_pressed():
        # The button is N/O and pulled high when open, the button is active low
        pub.sendMessage(str(Launch.Event.START_BUTTON_PRESSED))

    @staticmethod
    def _on_difficulty_pin_change(pin: int, value: int):
        # TODO: fill out difficulty calculation logic
        pub.sendMessage(str(Launch.Event.DIFFICULTY_CHANGED))

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    @staticmethod
    def sub_key_toggle(listener: Callable):
        pub.subscribe(listener, str(Launch.Event.KEY_TOGGLE))

    @staticmethod
    def sub_estop_toggle(listener: Callable):
        pub.subscribe(listener, str(Launch.Event.ESTOP_TOGGLE))

    @staticmethod
    def sub_start_pressed(listener: Callable):
        pub.subscribe(listener, str(Launch.Event.START_BUTTON_PRESSED))

    @staticmethod
    def sub_difficulty_change(listener: Callable):
        pub.subscribe(listener, str(Launch.Event.DIFFICULTY_CHANGED))
