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
        # ---- Class Values ----
        self.x_axis = 0  # Range 0 - 1
        self.y_axis = 0  # Range 0 - 1

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
        button_state = states.Button.PRESSED if value == 0 else states.Button.RELEASED

        match pin:
            case self._track_jam_pin:
                self.track_jam = button_state
                pub.sendMessage(self._track_jam_event())

            case self._auto_cycle_start_pin:
                self.auto_cycle_start = button_state
                pub.sendMessage(self._auto_cycle_start_event())

            case self._split_normal_pin:
                self.split_normal = button_state
                pub.sendMessage(self._split_normal_event())

            case self._auto_manual_pin:
                self.auto_manual = button_state
                pub.sendMessage(self._auto_manual_event())

            case self._warp_drive_pin:
                self.warp_drive = button_state
                pub.sendMessage(self._warp_drive_event())

            case self._thruster_left_pin:
                self.thruster_left = button_state
                pub.sendMessage(self._rcs_thruster_event(), direction=-1)
            case self._thruster_right_pin:
                self.thruster_right = button_state
                pub.sendMessage(self._rcs_thruster_event(), direction=-1)

            case self._stop_button_pin:
                self.stop_button = button_state
                pub.sendMessage(self._stop_button_event())

            case self._one_button_pin:
                self.one_button = button_state
                pub.sendMessage(self._one_button_event())

            case self._two_button_pin:
                self.two_button = button_state
                pub.sendMessage(self._two_button_event())

            case self._y_axis_invert_pin:
                self.y_axis_invert = button_state
                pub.sendMessage(self._y_axis_invert_event())

    def _on_analog_change(self, pin: int, value: int) -> None:
        """
        Callback for when one of the analog pins in the flight control panel is activated (active low, 0).

        :param pin:
        :param value:
        """
        normalized_value = value / 65535.

        match pin:
            case self._x_axis_pin:
                self.x_axis = normalized_value
                pub.sendMessage(self._joystick_event(), x=self.x_axis, y=self.y_axis)

            case self._y_axis_pin:
                self.y_axis = normalized_value
                pub.sendMessage(self._joystick_event(), x=self.x_axis, y=self.y_axis)

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def _track_jam_event(self):
        return self._event_name(FlightControl.Event.TRACK_JAM_PRESSED, self._track_jam_pin)

    def sub_track_jam_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the track jam button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._track_jam_event())

    def unsub_track_jam_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the track jam button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._track_jam_event())

    def _auto_cycle_start_event(self):
        return self._event_name(FlightControl.Event.AUTO_CYCLE_START_PRESSED, self._auto_cycle_start_pin)

    def sub_auto_cycle_start_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the auto cycle start button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._auto_cycle_start_event())

    def unsub_auto_cycle_start_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the auto cycle start button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._auto_cycle_start_event())

    def _split_normal_event(self):
        return self._event_name(FlightControl.Event.AUTO_CYCLE_START_PRESSED, self._auto_cycle_start_pin)

    def sub_split_normal_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the split normal button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._split_normal_event())

    def unsub_split_normal_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the split normal button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._split_normal_event())

    def _auto_manual_event(self):
        return self._event_name(FlightControl.Event.AUTO_MANUAL_PRESSED, self._auto_manual_pin)

    def sub_auto_manual_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the auto/manual button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._auto_manual_event())

    def unsub_auto_manual_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the auto/manual button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._auto_manual_event())

    def _warp_drive_event(self):
        return self._event_name(FlightControl.Event.WARP_DRIVE_ENGAGED, self._warp_drive_pin)

    def sub_warp_drive_engaged(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the warp drive switch being engaged.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._warp_drive_event())

    def unsub_warp_drive_engaged(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the warp drive switch being engaged.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._warp_drive_event())

    def _rcs_thruster_event(self):
        return self._event_name(
            FlightControl.Event.RCS_THRUSTER_TOGGLED,
            self._thruster_left_pin,
            self._thruster_right_pin)

    def sub_rcs_thruster_toggled(self, listener: Callable[[int], None]) -> None:
        """
        Subscribe to rcs thruster toggle switch being moved to the left, right, or center.

        :param listener:
            Callback function that takes the following arguments:
                - `direction` (`int`): The direction of the rcs thruster (-1 for left, 0 for center, 1 for right).
        """
        pub.subscribe(listener, self._rcs_thruster_event())

    def unsub_rcs_thruster_toggled(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to rcs thruster toggle switch being moved to the left, right, or center.

        :param listener:
            Callback function that takes the following arguments:
                - `direction` (`int`): The direction of the rcs thruster (-1 for left, 0 for center, 1 for right).
        """
        pub.unsubscribe(listener, self._rcs_thruster_event())

    def _stop_button_event(self):
        return self._event_name(FlightControl.Event.STOP_BUTTON_PRESSED, self._stop_button_pin)

    def sub_stop_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the stop button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._stop_button_event())

    def unsub_stop_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the stop button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._stop_button_event())

    def _one_button_event(self):
        return self._event_name(FlightControl.Event.ONE_BUTTON_PRESSED, self._one_button_pin)

    def sub_one_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the one button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._one_button_event())

    def unsub_one_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the one button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._one_button_event())

    def _two_button_event(self):
        return self._event_name(FlightControl.Event.TWO_BUTTON_PRESSED, self._two_button_pin)

    def sub_two_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the two button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._two_button_event())

    def unsub_two_button_pressed(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the two button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._two_button_event())

    def _y_axis_invert_event(self):
        return self._event_name(FlightControl.Event.Y_AXIS_INVERT_TOGGLED, self._y_axis_invert_pin)

    def sub_y_axis_invert_toggled(self, listener: Callable[[], None]) -> None:
        """
        Subscribe to the y-axis invert switch being toggled.

        :param listener: Callback function that takes no arguments.
        """
        pub.subscribe(listener, self._y_axis_invert_event())

    def unsub_y_axis_invert_toggled(self, listener: Callable[[], None]) -> None:
        """
        Unsubscribe to the two button being pressed.

        :param listener: Callback function that takes no arguments.
        """
        pub.unsubscribe(listener, self._y_axis_invert_event())

    def _joystick_event(self) -> str:
        return self._event_name(FlightControl.Event.JOYSTICK_MOVE, self._x_axis_pin, self._y_axis_pin)

    def sub_joystick_moved(self, listener: Callable[[float, float], None]) -> None:
        """
        Subscribe to the y-axis invert switch being toggled.

        :param listener: Callback function that takes the following arguments.
            - `x` (`float`): The x-axis value from 0 to 1
            - `y` (`float`): The y-axis value from 0 to 1
        """
        pub.subscribe(listener, self._joystick_event())

    def unsub_joystick_moved(self, listener: Callable[[float, float], None]) -> None:
        """
        Unsubscribe to the two button being pressed.

        :param listener: Callback function that takes the following arguments.
            - `x` (`float`): The x-axis value from 0 to 1
            - `y` (`float`): The y-axis value from 0 to 1
        """
        pub.unsubscribe(listener, self._joystick_event())

    @staticmethod
    def _event_name(event: Event, pin: int, pin2: int = 0):
        if pin2 == 0:
            return f'{event}_{pin}'
        else:
            return f'{event}_{pin}_{pin2}'
