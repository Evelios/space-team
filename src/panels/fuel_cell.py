from enum import Enum, auto
from typing import Callable
from pubsub import pub

from hardware.pin_manager import PinManager


class FuelCell:
    """
    A fuel cell is the power for the engines. Each fuel cell can be activated or deactivated, as well as be faulted
    while on.
    """

    class Event(Enum):
        TURNED_ON = auto()
        TURNED_OFF = auto()
        FAULTED = auto()
        CLEARED_FAULT = auto()

    class State(Enum):
        """ Fuel cell state tracks how the fuel cell is operating. """
        ON = auto()
        OFF = auto()
        FAULT = auto()

    def __init__(self, on_off_pin: int, cycle_pin: int):
        self.on_off_pin = on_off_pin
        self.cycle_pin = cycle_pin
        self.state = FuelCell.State.OFF

        # Setup event triggers for the on/off switch and the cycle engine button
        PinManager.sub_digital_change(self.on_off_pin, self._on_off_switch_toggled)
        PinManager.sub_digital_falling(self.cycle_pin, self._cycle_button_pressed)

    # ---- Event Handling ----------------------------------------------------------------------------------------------

    def _on_off_switch_toggled(self, on_off_pin_state: int) -> None:
        """
        Triggered event that is run whenever the fuel cell on/off switch changes.
        Update the fuel cell state to correlate with the on/off switch state.

        :param on_off_pin_state: The state of the on/off switch. The switch is active low (0) when the switch is on.
        """
        if on_off_pin_state == 0:
            self.state = FuelCell.State.ON
            pub.sendMessage(FuelCell._event_name(FuelCell.Event.TURNED_ON, self.on_off_pin))
        else:
            self.state = FuelCell.State.OFF
            pub.sendMessage(FuelCell._event_name(FuelCell.Event.TURNED_OFF, self.on_off_pin))

    def _cycle_button_pressed(self, cycle_pin_state: int) -> None:
        """
        Triggered event that is run whenever the engine cycle switch changes.
        Update the fuel cell state to correlate with the cycle switch state.
        If the fuel cell was cycled, the fuel cell fault will be cleared.

        :param cycle_pin_state:
        """

        if cycle_pin_state == 1 and self.state == FuelCell.State.FAULT:
            self.state = FuelCell.State.ON

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def sub_turned_on(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to when the Fuel Cell is turned on.

        :param listener: Callable that takes no arguments
        """
        pub.subscribe(listener, FuelCell._event_name(FuelCell.Event.TURNED_ON, self.on_off_pin))

    def sub_turned_off(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to when the Fuel Cell is turned off.

        :param listener: Callable that takes no arguments
        """
        pub.subscribe(listener, FuelCell._event_name(FuelCell.Event.TURNED_OFF, self.on_off_pin))

    def sub_faulted(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to when the Fuel Cell is faulted.

        :param listener: Callable that takes no arguments
        """
        pub.subscribe(listener, FuelCell._event_name(FuelCell.Event.FAULTED, self.on_off_pin))

    def sub_cleared_fault(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to when the Fuel Cell fault is cleared

        :param listener: Callable that takes no arguments
        """
        pub.subscribe(listener, FuelCell._event_name(FuelCell.Event.CLEARED_FAULT, self.on_off_pin))

    @staticmethod
    def _event_name(event: Event, event_id: int) -> str:
        """
        Create and event name for publishing and subscribing.

        :param event: The event that is being called
        :param event_id: A unique identifier to this class that will be added to the event name
        :return: An event name that can be used for publishing and subscribing to
        """

        return f"FuelCell_{event_id}.{event}"
