from enum import Enum, auto
from pubsub import pub
from typing import Callable

from hardware.pin_manager import PinManager
from hardware import states


class FlightControl:
    """
    Flight Control Panel. This panel contains controls for the shuttles flight heading, drive modes, flight modes, and
    rcs thrusters.
    """

    class DriveButton(Enum):
        TRACK_JAM = auto()
        AUTO_CYCLE_START = auto()
        SPLIT_NORMAL = auto()
        AUTO_MANUAL = auto()

    class FlightMode(Enum):
        ONE = auto()
        TWO = auto()
        STOP = auto()

    class Event(Enum):
        TRACK_JAM_PRESSED = auto()
        AUTO_CYCLE_START_PRESSED = auto()
        SPLIT_NORMAL_PRESSED = auto()
        AUTO_MANUAL_PRESSED = auto()
        WARP_DRIVE_ENGAGED = auto()
        RCS_THRUSTER_TOGGLED = auto()
        STOP_BUTTON_PRESSED = auto()
        ONE_BUTTON_PRESSED = auto()
        TWO_BUTTON_PRESSED = auto()
        Y_AXIS_INVERT_TOGGLED = auto()
        JOYSTICK_MOVE = auto()

    def __init__(self):
        # ---- Pin Assignments ----
        self._track_jam_pin = 5
        self._auto_cycle_start_pin = 6
        self._split_normal_pin = 7
        self._auto_manual_pin = 8
        self._warp_drive_pin = 9
        self._thruster_left_pin = 10
        self._thruster_right_pin = 11
        self._stop_button_pin = 12
        self._one_button_pin = 13
        self._two_button_pin = 14
        self._y_axis_invert_pin = 15
        self._x_axis_pin = 1
        self._y_axis_pin = 2

        # ---- Initial Pin States ----
        self.track_jam = states.Button.RELEASED
        self.auto_cycle_start = states.Button.RELEASED
        self.split_normal = states.Button.RELEASED
        self.auto_manual = states.Button.RELEASED
        self.warp_drive = states.Button.RELEASED
        self.thruster_left = states.Button.RELEASED
        self.thruster_right = states.Button.RELEASED
        self.stop_button = states.Button.RELEASED
        self.one_button = states.Button.RELEASED
        self.two_button = states.Button.RELEASED
        self.y_axis_invert = states.Button.RELEASED
        self.x_axis = 0
        self.y_axis = 0

        # ---- Pin Change Event Subscriptions ----
        PinManager.sub_digital_change(self._track_jam_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._auto_cycle_start_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._split_normal_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._auto_manual_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._warp_drive_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._thruster_left_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._thruster_right_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._stop_button_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._one_button_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._two_button_pin, self._on_digital_change)
        PinManager.sub_digital_change(self._y_axis_invert_pin, self._on_digital_change)
        PinManager.sub_analog_change(self._x_axis_pin, self._on_analog_change)
        PinManager.sub_analog_change(self._y_axis_pin, self._on_analog_change)

    # ---- Event Handling ----------------------------------------------------------------------------------------------

    def _on_digital_change(self, pin: int, value: int) -> None:
        """
        Callback for when one of the digital pins in the flight control panel is activated (active low, 0).

        :param pin:
        :param value:
        """

    def _on_analog_change(self, pin: int, value: int) -> None:
        """
        Callback for when one of the analog pins in the flight control panel is activated (active low, 0).

        :param pin:
        :param value:
        """

    def _on_y_axis_change(self, pin: int, value: float) -> None:
        pass

    def _on_x_axis_change(self, pin: int, value: float) -> None:
        pass

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def sub_track_jam_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the track jam button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.TRACK_JAM_PRESSED, self._track_jam_pin)
        pub.subscribe(listener, event_name)

    def unsub_track_jam_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the track jam button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.TRACK_JAM_PRESSED, self._track_jam_pin)
        pub.unsubscribe(listener, event_name)

    def sub_auto_cycle_start_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the auto cycle start button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.AUTO_CYCLE_START_PRESSED, self._auto_cycle_start_pin)
        pub.subscribe(listener, event_name)

    def unsub_auto_cycle_start_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the auto cycle start button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.AUTO_CYCLE_START_PRESSED, self._auto_cycle_start_pin)
        pub.unsubscribe(listener, event_name)

    def sub_split_normal_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the split normal button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.AUTO_CYCLE_START_PRESSED, self._auto_cycle_start_pin)
        pub.subscribe(listener, event_name)

    def unsub_split_normal_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the split normal button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.AUTO_CYCLE_START_PRESSED, self._auto_cycle_start_pin)
        pub.unsubscribe(listener, event_name)

    def sub_auto_manual_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the auto/manual button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.AUTO_MANUAL_PRESSED, self._auto_manual_pin)
        pub.subscribe(listener, event_name)

    def unsub_auto_manual_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the auto/manual button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.AUTO_MANUAL_PRESSED, self._auto_manual_pin)
        pub.unsubscribe(listener, event_name)

    def sub_warp_drive_engaged(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the warp drive switch being engaged.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.WARP_DRIVE_ENGAGED, self._warp_drive_pin)
        pub.subscribe(listener, event_name)

    def unsub_warp_drive_engaged(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the warp drive switch being engaged.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.WARP_DRIVE_ENGAGED, self._warp_drive_pin)
        pub.unsubscribe(listener, event_name)

    def sub_rcs_thruster_toggled(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to rcs thruster toggle switch being moved to the left, right, or center.

        :param listener:
            Callback function that takes the following arguments:
                - `direction` (`int`): The direction of the rcs thruster (-1 for left, 0 for center, 1 for right).
        """
        event_name = self._event_name(
            FlightControl.Event.RCS_THRUSTER_TOGGLED,
            self._thruster_left_pin,
            self._thruster_right_pin)

        pub.subscribe(listener, event_name)

    def unsub_rcs_thruster_toggled(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to rcs thruster toggle switch being moved to the left, right, or center.

        :param listener:
            Callback function that takes the following arguments:
                - `direction` (`int`): The direction of the rcs thruster (-1 for left, 0 for center, 1 for right).
        """
        event_name = self._event_name(
            FlightControl.Event.RCS_THRUSTER_TOGGLED,
            self._thruster_left_pin,
            self._thruster_right_pin)

        pub.unsubscribe(listener, event_name)

    def sub_stop_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the stop button button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.STOP_BUTTON_PRESSED, self._stop_button_pin)
        pub.subscribe(listener, event_name)

    def sub_one_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the one button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.ONE_BUTTON_PRESSED, self._one_button_pin)
        pub.subscribe(listener, event_name)

    def unsub_one_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the one button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.ONE_BUTTON_PRESSED, self._one_button_pin)
        pub.unsubscribe(listener, event_name)

    def sub_two_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the two button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.TWO_BUTTON_PRESSED, self._two_button_pin)
        pub.subscribe(listener, event_name)

    def unsub_two_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the two button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        event_name = self._event_name(FlightControl.Event.TWO_BUTTON_PRESSED, self._two_button_pin)
        pub.unsubscribe(listener, event_name)

    @staticmethod
    def _event_name(event: Event, pin: int, pin2: int = 0):
        if pin2 == 0:
            return f'{event}_{pin}'
        else:
            return f'{event}_{pin}_{pin2}'
