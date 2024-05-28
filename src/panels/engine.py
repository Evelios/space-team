from enum import Enum, auto
from machine import I2C

from hardware.pin_manager import PinManager


class FuelCell:
    """
    A fuel cell is the power for the engines. Each fuel cell can be activated or deactivated, as well as be faulted
    while on.
    """

    class State(Enum):
        """ Fuel cell state tracks how the fuel cell is operating. """
        ON = auto()
        OFF = auto()
        FAULT = auto()

    def __init__(self, pin_manager: PinManager, on_off_pin: int, cycle_pin: int):
        self.pin_manager = pin_manager
        self.on_off_pin = on_off_pin
        self.cycle_pin = cycle_pin
        self.state = FuelCell.State.OFF

        # Setup event triggers for the on/off switch and the cycle engine button
        pin_manager.on_digital_change(self.on_off_pin, self.on_off_pin_changed)
        pin_manager.on_digital_change(self.on_off_pin, self.cycle_pin_changed)

    def on_off_pin_changed(self, on_off_pin_state: int) -> None:
        """
        Triggered event that is run whenever the fuel cell on/off switch changes.
        Update the fuel cell state to correlate with the on/off switch state.

        :param on_off_pin_state:
        """
        if on_off_pin_state == 1:
            self.state = FuelCell.State.ON
        else:
            self.state = FuelCell.State.OFF

    def cycle_pin_changed(self, cycle_pin_state: int) -> None:
        """
        Triggered event that is run whenever the engine cycle switch changes.
        Update the fuel cell state to correlate with the cycle switch state.
        If the fuel cell was cycled, the fuel cell fault will be cleared.

        :param cycle_pin_state:
        :return:
        """

        if cycle_pin_state == 1 and self.state == FuelCell.State.FAULT:
            self.state = FuelCell.State.ON


class Engine:
    """
    Engine panel
    """

    def __init__(self, pinmanager: PinManager, i2c: I2C):
        """
        :param pinmanager:
        :param i2c:
        """
        self.engine_on_off_pin = 28

        self.fuel_cell1 = FuelCell(pinmanager, on_off_pin=29, cycle_pin=33)
        self.fuel_cell1 = FuelCell(pinmanager, on_off_pin=30, cycle_pin=34)
        self.fuel_cell1 = FuelCell(pinmanager, on_off_pin=31, cycle_pin=35)
        self.fuel_cell1 = FuelCell(pinmanager, on_off_pin=32, cycle_pin=36)

        self.lcd = None
