from typing import Callable

from hardware.pin_manager import PinManager
from hardware import states
from pubsub.publisher import Publisher


class Launch:
    """
    Launch panel
    """

    class Event:
        KEY_TOGGLE = 'Launch.KeyToggle'
        ESTOP_TOGGLE = 'Launch.EstopToggle'
        START_BUTTON_PRESSED = 'Launch.StartButtonPressed'
        DIFFICULTY_CHANGED = 'Launch.DifficultyChanged'

    def __init__(self, pin_manager: PinManager):
        self.pin_manager = pin_manager
        self.publisher = Publisher()

        # ---- Class Values ----
        self.difficulty = 0

        # ---- Pin Assignments ----
        self._key_pin = 40
        self._start_pin = 38
        self._estop_pin = 39
        self._mileage_pin = 37
        self._difficulty_pins = list(range(41, 47))

        # ---- Initial Pin States ----
        self.key = states.Button.RELEASED
        self.start = states.Button.RELEASED
        self.estop = states.Button.RELEASED

        # ---- Pin Change Event Subscriptions ----
        self.pin_manager.sub_digital_change(self._key_pin, self._on_digital_change)
        self.pin_manager.sub_digital_change(self._estop_pin, self._on_digital_change)
        self.pin_manager.sub_digital_change(self._start_pin, self._on_digital_change)

        for pin in self._difficulty_pins:
            self.pin_manager.sub_digital_change(pin, self._on_digital_change)

    # ---- Modifiers ---------------------------------------------------------------------------------------------------

    def _on_digital_change(self, pin: int, value: int) -> None:
        button_state = states.Button.PRESSED if value == 0 else states.Button.RELEASED

        match pin:
            case self._key_pin:
                self.key = button_state
                self.publisher.send_message(self._key_event())

            case self._estop_pin:
                self.estop = button_state
                self.publisher.send_message(self._estop_event())

            case _ if pin in self._difficulty_pins:
                # TODO: Difficulty calculation
                pass

    def _calculate_difficulty(self) -> int:
        return 0

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def _key_event(self):
        return self._event_name(Launch.Event.KEY_TOGGLE, pin=self._key_pin)

    def sub_key_toggle(self, listener: Callable[[int], None]) -> None:
        """
        Subscribe to the start key outlet being turned on or off.

        :param listener: Callback function taking the following arguments.
            - `state` (`SwitchState`): Current state of the switch
        """
        self.publisher.subscribe(self._key_event(), listener)

    def unsub_key_toggle(self, listener: Callable[[int], None]) -> None:
        """
        Unsubscribe to the start key outlet being turned on or off.

        :param listener: Callback function taking the following arguments.
            - `state` (`SwitchState`): Current state of the switch
        """
        self.publisher.unsubscribe(self._key_event(), listener)

    def _estop_event(self):
        return self._event_name(Launch.Event.ESTOP_TOGGLE, pin=self._estop_pin)

    def sub_estop_toggle(self, listener: Callable[[states.Switch], None]) -> None:
        """
        Subscribe to the estop button being engaged (pressed) or disengaged (released)

        :param listener: Callback function taking the following arguments.
            - `state` (`Switch`): Current state of the switch
        """
        self.publisher.subscribe(self._estop_event(), listener)

    def unsub_estop_toggle(self, listener: Callable[[states.Switch], None]) -> None:
        """
        Unsubscribe to the estop button being engaged (pressed) or disengaged (released)

        :param listener: Callback function taking the following arguments.
            - `state` (`Switch`): Current state of the switch
        """
        self.publisher.unsubscribe(self._estop_event(), listener)

    def _start_event(self):
        return self._event_name(Launch.Event.START_BUTTON_PRESSED, pin=self._start_pin)

    def sub_start_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the start button being pressed.

        :param listener: Callback function taking no arguments.
        """
        self.publisher.subscribe(self._start_event(), listener)

    def unsub_start_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the start button being pressed.

        :param listener: Callback function taking no arguments.
        """
        self.publisher.unsubscribe(self._start_event(), listener)

    def _difficulty_event(self):
        return self._event_name(Launch.Event.DIFFICULTY_CHANGED, pin=self._difficulty_pins[0])

    def sub_difficulty_change(self, listener: Callable[[int], None]) -> None:
        """
        Subscribe to the start button being pressed.

        :param listener: Callback function taking the following arguments.
            - `difficulty` (`int`): Current difficulty from the launch panel
        """
        self.publisher.subscribe(self._difficulty_event(), listener)

    def unsub_difficulty_change(self, listener: Callable[[int], None]) -> None:
        """
        Unsubscribe to the start button being pressed.

        :param listener: Callback function taking the following arguments.
            - `difficulty` (`int`): Current difficulty from the launch panel
        """
        self.publisher.unsubscribe(self._difficulty_event(), listener)

    @staticmethod
    def _event_name(event: str, pin: int):
        return f'{event}_{pin}'
