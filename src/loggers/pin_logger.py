from .log import Log
from hardware.pin_manager import PinManager


class PinLogger:

    def __init__(self, pin_manager: PinManager):
        self.pin_manager = pin_manager

        Log.info('Pin Logger initialized. Watching 62 Digital Pins & 18 Analog Pins.')

        for pin in range(1, 65):
            self.pin_manager.sub_digital_rising(pin, PinLogger.on_digital_change)

        for pin in range(1, 17):
            self.pin_manager.sub_analog_change(pin, PinLogger.on_analog_change)

        # Make sure to add the two analog pins in the digital bus
        self.pin_manager.sub_analog_change(47, PinLogger.on_analog_change)
        self.pin_manager.sub_analog_change(48, PinLogger.on_analog_change)

    @staticmethod
    def on_digital_change(pin: int) -> None:
        Log.debug(f'Digital Change on Pin: {pin}')

    @staticmethod
    def on_analog_change(pin: int, value: int) -> None:
        Log.debug(f"Analog Pin Change: {pin} at {value}")
