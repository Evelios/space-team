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
        self._key_pin = 40
        self._start_pin = 38
        self._estop_pin = 39
        self._mileage_pin = 37

        self._difficulty_pins = list(range(41, 47))
        self.difficulty = 0

        PinManager.sub_digital_change(self._key_pin, self._on_key_toggle)
        PinManager.sub_digital_change(self._estop_pin, self._on_estop_toggle)
        PinManager.sub_digital_falling(self._start_pin, self._on_start_button_pressed)

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

    def _on_difficulty_pin_change(self, pin: int, value: int):
        # TODO: fill out difficulty calculation logic
        self.difficulty = 0
        pub.sendMessage(str(Launch.Event.DIFFICULTY_CHANGED), self.difficulty)

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def sub_key_toggle(self, listener: Callable[[int], None]) -> None:
        """
        Subscribe to the start key outlet being turned on or off.

        :param listener: Callback function taking the following arguments.
            - `state` (`SwitchState`): Current state of the switch
        """
        event_name = self._event_name(Launch.Event.KEY_TOGGLE, self._key_pin)
        pub.subscribe(listener, event_name)

    def unsub_key_toggle(self, listener: Callable[[int], None]) -> None:
        """
        Unsubscribe to the start key outlet being turned on or off.

        :param listener: Callback function taking the following arguments.
            - `state` (`SwitchState`): Current state of the switch
        """
        event_name = self._event_name(Launch.Event.KEY_TOGGLE, self._key_pin)
        pub.unsubscribe(listener, event_name)

    def sub_estop_toggle(self, listener: Callable[[states.Switch], None]) -> None:
        """
        Subscribe to the estop button being engaged (pressed) or disengaged (released)

        :param listener: Callback function taking the following arguments.
            - `state` (`Switch`): Current state of the switch
        """
        event_name = self._event_name(Launch.Event.ESTOP_TOGGLE, self._estop_pin)
        pub.subscribe(listener, event_name)

    def unsub_estop_toggle(self, listener: Callable[[states.Switch], None]) -> None:
        """
        Unsubscribe to the estop button being engaged (pressed) or disengaged (released)

        :param listener: Callback function taking the following arguments.
            - `state` (`Switch`): Current state of the switch
        """
        event_name = self._event_name(Launch.Event.ESTOP_TOGGLE, self._estop_pin)
        pub.subscribe(listener, event_name)

    def sub_start_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the start button being pressed.

        :param listener: Callback function taking no arguments.
        """
        event_name = self._event_name(Launch.Event.START_BUTTON_PRESSED, self._start_pin)
        pub.subscribe(listener, event_name)

    def unsub_start_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the start button being pressed.

        :param listener: Callback function taking no arguments.
        """
        event_name = self._event_name(Launch.Event.START_BUTTON_PRESSED, self._start_pin)
        pub.unsubscribe(listener, event_name)

    def sub_difficulty_change(self, listener: Callable[[int], None]) -> None:
        """
        Subscribe to the start button being pressed.

        :param listener: Callback function taking the following arguments.
            - `difficulty` (`int`): Current difficulty from the launch panel
        """
        event_name = self._event_name(Launch.Event.DIFFICULTY_CHANGED, self._difficulty_pins[0])
        pub.subscribe(listener, event_name)

    def unsub_difficulty_change(self, listener: Callable[[int], None]) -> None:
        """
        Unsubscribe to the start button being pressed.

        :param listener: Callback function taking the following arguments.
            - `difficulty` (`int`): Current difficulty from the launch panel
        """
        event_name = self._event_name(Launch.Event.DIFFICULTY_CHANGED, self._difficulty_pins[0])
        pub.unsubscribe(listener, event_name)

    @staticmethod
    def _event_name(event: Event, pin: int):
        return f'{event}_{pin}'
