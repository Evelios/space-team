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
        HOLD = auto()

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
        button_state = states.Button.PRESSED if value == 0 else states.Button.RELEASED

        match pin:
            case self._airflow_pin:
                self.airflow = button_state
                pub.sendMessage(self._airflow_event(), state=self.airflow)

            case self._pressure_pin:
                self.pressure = button_state
                if button_state == states.Button.PRESSED:
                    pub.sendMessage(self._pressure_event(), state=self.pressure)

            case self._oxygen_pin:
                self.oxygen = button_state
                pub.sendMessage(self._oxygen_event(), state=self.oxygen)

            case self._void_waste_pin:
                self.void_waste = button_state
                if button_state == states.Button.PRESSED:
                    pub.sendMessage(self._void_waste_event(), state=self.void_waste)

            case self._cabin_pressure_on_pin if button_state == states.Button.PRESSED:
                self.cabin_pressure = ECS.CabinPressureState.ON
                pub.sendMessage(self._cabin_pressure_event(), state=self.cabin_pressure)

            case self._cabin_pressure_off_pin if button_state == states.Button.PRESSED:
                self.cabin_pressure = ECS.CabinPressureState.OFF
                pub.sendMessage(self._cabin_pressure_event(), state=self.cabin_pressure)

            case self._cabin_pressure_hold_pin if button_state == states.Button.PRESSED:
                self.cabin_pressure = ECS.CabinPressureState.HOLD
                pub.sendMessage(self._cabin_pressure_event(), state=self.cabin_pressure)

    # ---- Subscriptions -----------------------------------------------------------------------------------------------
    def _airflow_event(self):
        return self._event_name(ECS.Event.AIRFLOW_TOGGLE, self._airflow_pin)

    def sub_airflow_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Subscribe to the airflow button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        pub.subscribe(listener, self._airflow_event())

    def unsub_airflow_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Unsubscribe to the airflow button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        pub.unsubscribe(listener, self._airflow_event())

    def _pressure_event(self):
        return self._event_name(ECS.Event.PRESSURE_PRESSED, self._pressure_pin)

    def sub_pressure_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the pressure button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._pressure_event())

    def unsub_pressure_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the pressure button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._pressure_event())

    def _oxygen_event(self):
        return self._event_name(ECS.Event.OXYGEN_TOGGLE, self._oxygen_pin)

    def sub_oxygen_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Subscribe to the oxygen button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        pub.subscribe(listener, self._oxygen_event())

    def unsub_oxygen_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Unsubscribe to the oxygen button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        pub.unsubscribe(listener, self._oxygen_event())

    def _void_waste_event(self):
        return self._event_name(ECS.Event.VOID_WASTE_PRESSED, self._void_waste_pin)

    def sub_void_waste_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the void waste button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._void_waste_event())

    def unsub_void_waste_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the void waste button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._void_waste_event())

    def _cabin_pressure_event(self):
        return self._event_name(ECS.Event.CABIN_PRESSURE_TOGGLED, self._cabin_pressure_on_pin)

    def sub_cabin_pressure_toggled(self, listener: Callable[[CabinPressureState], None]) -> None:
        """
        Subscribe to the cabin pressure switch being toggled.

        :param listener: Callback function that takes the following arguments:
            - `state` (`CabinPressureState`) - The state of the cabin pressure toggle switch.

        """
        pub.subscribe(listener, self._cabin_pressure_event())

    def unsub_cabin_pressure_toggled(self, listener: Callable[[CabinPressureState], None]) -> None:
        """
        Unsubscribe to the cabin pressure switch being toggled.

        :param listener: Callback function that takes the following arguments:
            - `state` (`CabinPressureState`) - The state of the cabin pressure toggle switch.
        """
        pub.unsubscribe(listener, self._cabin_pressure_event())

    @staticmethod
    def _event_name(event: Event, pin: int) -> str:
        return f'{event}_{pin}'
