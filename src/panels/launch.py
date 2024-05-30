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
        self.difficulty = 0

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

    def _on_difficulty_pin_change(self, pin: int, value: int):
        # TODO: fill out difficulty calculation logic
        self.difficulty = 0
        pub.sendMessage(str(Launch.Event.DIFFICULTY_CHANGED), self.difficulty)

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    @staticmethod
    def sub_key_toggle(listener: Callable[[int], None]) -> None:
        """
        Subscribe to the start key outlet being turned on or off.

        :param listener: Callback function taking the following arguments.
            - `state` (`SwitchState`): Current state of the switch
        """
        pub.subscribe(listener, str(Launch.Event.KEY_TOGGLE))

    @staticmethod
    def sub_estop_toggle(listener: Callable[[states.Switch], None]) -> None:
        """
        Subscribe to the estop button being engaged (pressed) or disengaged (released)

        :param listener: Callback function taking the following arguments.
            - `state` (`Switch`): Current state of the switch
        """
        pub.subscribe(listener, str(Launch.Event.ESTOP_TOGGLE))

    @staticmethod
    def sub_start_button_pressed(listener: Callable[[], None]) -> None:
        """
        Subscribe to the start button being pressed.

        :param listener: Callback function taking no arguments.
        """
        pub.subscribe(listener, str(Launch.Event.START_BUTTON_PRESSED))

    @staticmethod
    def sub_difficulty_change(listener: Callable[[int], None]) -> None:
        """
        Subscribe to the start button being pressed.

        :param listener: Callback function taking the following arguments.
            - `difficulty` (`int`): Current difficulty from the launch panel
        """
        pub.subscribe(listener, str(Launch.Event.DIFFICULTY_CHANGED))
