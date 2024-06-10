import pubsub.pub
from machine import I2C
from pubsub import pub
from typing import Callable

from .fuel_cell import FuelCell
from hardware import states
from hardware.pin_manager import PinManager


class Engine:
    """
    Engine panel


    You can access each fuel cell individually from the engine, or access the fuel cells in list format.

    .. code-block::python

        engine = Engine(i2c)
        engine.fuel_cell1.fault() # Variable access
        engine.fuel_cell[0].fault() # List access to fault fuel cell 1
    """

    class Event:
        ON_OFF_TOGGLED = 'Engine.OnOffToggled'

    def __init__(self, i2c: I2C):
        """
        :param i2c: I2C connection on the board. This allows for connection of the engine to the LCD of the engine.
        """
        # ---- Fuel Cells ----
        self.fuel_cell1 = FuelCell(on_off_pin=29, cycle_pin=33)
        self.fuel_cell2 = FuelCell(on_off_pin=30, cycle_pin=34)
        self.fuel_cell3 = FuelCell(on_off_pin=31, cycle_pin=35)
        self.fuel_cell4 = FuelCell(on_off_pin=32, cycle_pin=36)

        # Allows for list indexing of fuel cells as well as variable access
        self.fuel_cells = [self.fuel_cell1, self.fuel_cell2, self.fuel_cell3, self.fuel_cell4]

        # ---- Pin Assignments ----
        self._engine_on_off_pin = 28

        # ---- Initial Pin States ----
        self.engine = states.Button.RELEASED

        # ---- Pin Change Event Subscriptions ----
        PinManager.sub_digital_change(self._engine_on_off_pin, self._on_off_toggle)

        self.lcd = None

    # ---- Event Handling ----------------------------------------------------------------------------------------------

    def _on_off_toggle(self, pin: int, value: int):
        """ Callback for when the on/off switch is toggled. """
        if value == 1:
            self.engine = states.Button.PRESSED
        else:
            self.engine = states.Button.RELEASED

        pubsub.pub.sendMessage(self._on_off_event(), state=self.engine)

    # ---- Subscriptions -----------------------------------------------------------------------------------------------

    def _on_off_event(self):
        return self._event_name(Engine.Event.ON_OFF_TOGGLED, self._engine_on_off_pin)

    def sub_cabin_pressure_toggled(self, listener: Callable[[states.Switch], None]) -> None:
        """
        Subscribe to on/off switch being toggled.

        :param listener: Callback function that takes the following arguments:
            - `state` (`states.Switch`) - The on/off switch state after being toggled
        """
        pub.subscribe(listener, self._on_off_event)

    def unsub_cabin_pressure_toggled(self, listener: Callable[[states.Switch], None]) -> None:
        """
        Subscribe to on/off switch being toggled.

        :param listener: Callback function that takes the following arguments:
            - `state` (`states.Switch`) - The on/off switch state after being toggled
        """
        pub.unsubscribe(listener, self._on_off_event)

    @staticmethod
    def _event_name(event: str, pin: int) -> str:
        return f'{event}_{pin}'
