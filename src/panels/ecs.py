from enum import Enum, auto
from pubsub import pub
from typing import Callable

from hardware import states
from hardware.pin_manager import PinManager


class ECS:
    """
    Environmental Control Systems Panel.
    """

    class CabinPressureState(Enum):
        ON = auto()
        OFF = auto()
        TOGGLE = auto()

    class Event(Enum):
        AIRFLOW_TOGGLE = auto()
        PRESSURE_PRESSED = auto()
        OXYGEN_TOGGLE = auto()
        VOID_WASTE_PRESSED = auto()
        CABIN_PRESSURE_TOGGLED = auto()

    def __init__(self):
        # ---- Pin Assignments ----
        self._airflow_pin = 21
        self._pressure_pin = 22
        self._oxygen_pin = 23
        self._void_waste_pin = 24
        self._cabin_pressure_on_pin = 25
        self._cabin_pressure_off_pin = 26
        self._cabin_pressure_hold_pin = 27

        # ---- Initial Pin States ----
        self.airflow = states.Button.RELEASED
        self.pressure = states.Button.RELEASED
        self.oxygen = states.Button.RELEASED
        self.void_waste = states.Button.RELEASED
        self.cabin_pressure = ECS.CabinPressureState.OFF

        # ---- Pin Change Event Subscriptions ----
        PinManager.sub_digital_change(self._airflow_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._pressure_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._oxygen_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._void_waste_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._cabin_pressure_on_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._cabin_pressure_off_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._cabin_pressure_hold_pin, self._on_digital_change)

    # ---- Event Handling ----------------------------------------------------------------------------------------------

    def _on_digital_change(self, pin: int, value: int):
        """
        Callback for when one of the digital pins in the flight control panel is activated (active low, 0).

        :param pin:
        :param value:
        """

    # ---- Subscriptions -----------------------------------------------------------------------------------------------
    def sub_airflow_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Subscribe to the airflow button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        event_name = self._event_name(ECS.Event.AIRFLOW_TOGGLE, self._airflow_pin)
        pub.subscribe(listener, event_name)

    def sub_pressure_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the pressure button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(ECS.Event.PRESSURE_PRESSED, self._pressure_pin)
        pub.subscribe(listener, event_name)

    def sub_oxygen_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Subscribe to the oxygen button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        event_name = self._event_name(ECS.Event.OXYGEN_TOGGLE, self._oxygen_pin)
        pub.subscribe(listener, event_name)

    def sub_void_waste_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the void waste button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(ECS.Event.VOID_WASTE_PRESSED, self._void_waste_pin)
        pub.subscribe(listener, event_name)

    def sub_cabin_pressure_toggled(self, listener: Callable[[CabinPressureState], None]) -> None:
        """
        Subscribe to the cabin pressure switch being toggled.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(ECS.Event.CABIN_PRESSURE_TOGGLED, self._cabin_pressure_on_pin)
        pub.subscribe(listener, event_name)

    @staticmethod
    def _event_name(event: Event, pin: int):
        return f'{event}_{pin}'
