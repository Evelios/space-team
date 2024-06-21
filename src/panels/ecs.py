from typing import Callable

from pubsub.publisher import Publisher
from hardware import states
from hardware.pin_manager import PinManager


class ECS:
    """
    Environmental Control Systems Panel.
    """

    class CabinPressureState:
        ON = 'Ecs.CabinPressure.On'
        OFF = 'Ecs.CabinPressure.Off'
        HOLD = 'Ecs.CabinPressure.Hold'

    class Event:
        AIRFLOW_TOGGLE = 'Ecs.AirflowToggle'
        PRESSURE_PRESSED = 'Ecs.PressurePressed'
        OXYGEN_TOGGLE = 'Ecs.OxygenToggle'
        VOID_WASTE_PRESSED = 'Ecs.VoidWastePressed'
        CABIN_PRESSURE_TOGGLED = 'Ecs.CabinPressureToggled'

    def __init__(self, pin_manager: PinManager):
        self.publisher = Publisher()
        self.pin_manager = pin_manager

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
        self.pin_manager.sub_digital_change(self._airflow_pin, self._on_digital_change)
        self.pin_manager.sub_digital_change(self._pressure_pin, self._on_digital_change)
        self.pin_manager.sub_digital_change(self._oxygen_pin, self._on_digital_change)
        self.pin_manager.sub_digital_change(self._void_waste_pin, self._on_digital_change)
        self.pin_manager.sub_digital_change(self._cabin_pressure_on_pin, self._on_digital_change)
        self.pin_manager.sub_digital_change(self._cabin_pressure_off_pin, self._on_digital_change)
        self.pin_manager.sub_digital_change(self._cabin_pressure_hold_pin, self._on_digital_change)

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
                self.publisher.send_message(self._airflow_event(), state=self.airflow)

            case self._pressure_pin:
                self.pressure = button_state
                if button_state == states.Button.PRESSED:
                    self.publisher.send_message(self._pressure_event(), state=self.pressure)

            case self._oxygen_pin:
                self.oxygen = button_state
                self.publisher.send_message(self._oxygen_event(), state=self.oxygen)

            case self._void_waste_pin:
                self.void_waste = button_state
                if button_state == states.Button.PRESSED:
                    self.publisher.send_message(self._void_waste_event(), state=self.void_waste)

            case self._cabin_pressure_on_pin if button_state == states.Button.PRESSED:
                self.cabin_pressure = ECS.CabinPressureState.ON
                self.publisher.send_message(self._cabin_pressure_event(), state=self.cabin_pressure)

            case self._cabin_pressure_off_pin if button_state == states.Button.PRESSED:
                self.cabin_pressure = ECS.CabinPressureState.OFF
                self.publisher.send_message(self._cabin_pressure_event(), state=self.cabin_pressure)

            case self._cabin_pressure_hold_pin if button_state == states.Button.PRESSED:
                self.cabin_pressure = ECS.CabinPressureState.HOLD
                self.publisher.send_message(self._cabin_pressure_event(), state=self.cabin_pressure)

    # ---- Subscriptions -----------------------------------------------------------------------------------------------
    def _airflow_event(self):
        return self._event_name(ECS.Event.AIRFLOW_TOGGLE, self._airflow_pin)

    def sub_airflow_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Subscribe to the airflow button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        self.publisher.subscribe(self._airflow_event(), listener)

    def unsub_airflow_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Unsubscribe to the airflow button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        self.publisher.unsubscribe(self._airflow_event(), listener)

    def _pressure_event(self):
        return self._event_name(ECS.Event.PRESSURE_PRESSED, self._pressure_pin)

    def sub_pressure_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the pressure button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        self.publisher.subscribe(self._pressure_event(), listener)

    def unsub_pressure_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the pressure button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        self.publisher.unsubscribe(self._pressure_event(), listener)

    def _oxygen_event(self):
        return self._event_name(ECS.Event.OXYGEN_TOGGLE, self._oxygen_pin)

    def sub_oxygen_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Subscribe to the oxygen button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        self.publisher.subscribe(self._oxygen_event(), listener)

    def unsub_oxygen_toggled(self, listener: Callable[[states.Button], None]) -> None:
        """
        Unsubscribe to the oxygen button being toggled.

        :param listener: Callback function that takes the following arguments.
             - `state` (`states.Button`) - The current toggleable button state
        """
        self.publisher.unsubscribe(self._oxygen_event(), listener)

    def _void_waste_event(self):
        return self._event_name(ECS.Event.VOID_WASTE_PRESSED, self._void_waste_pin)

    def sub_void_waste_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the void waste button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        self.publisher.subscribe(self._void_waste_event(), listener)

    def unsub_void_waste_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the void waste button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        self.publisher.unsubscribe(self._void_waste_event(), listener)

    def _cabin_pressure_event(self):
        return self._event_name(ECS.Event.CABIN_PRESSURE_TOGGLED, self._cabin_pressure_on_pin)

    def sub_cabin_pressure_toggled(self, listener: Callable[[CabinPressureState], None]) -> None:
        """
        Subscribe to the cabin pressure switch being toggled.

        :param listener: Callback function that takes the following arguments:
            - `state` (`CabinPressureState`) - The state of the cabin pressure toggle switch.

        """
        self.publisher.subscribe(self._cabin_pressure_event(), listener)

    def unsub_cabin_pressure_toggled(self, listener: Callable[[CabinPressureState], None]) -> None:
        """
        Unsubscribe to the cabin pressure switch being toggled.

        :param listener: Callback function that takes the following arguments:
            - `state` (`CabinPressureState`) - The state of the cabin pressure toggle switch.
        """
        self.publisher.unsubscribe(self._cabin_pressure_event(), listener)

    @staticmethod
    def _event_name(event: str, pin: int) -> str:
        return f'{event}_{pin}'
