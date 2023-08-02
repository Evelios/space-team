from machine import Pin, ADC


class Settings:
    """
    Settings control panel
    """

    def __init__(self, volume_pin: int, rumble_pin: int, invert_pin: int):
        """

        :param volume_pin:
        :param rumble_pin:
        :param invert_pin:
        """

        self.volume = ADC(Pin(volume_pin))
        self.rumble = ADC(Pin(rumble_pin))
        self.invert_y = Pin(invert_pin)

    def volume(self) -> int:
        """

        :return: The volume in the range 0 to 65535
        """
        return self.volume.read_u16()

    def rumble(self) -> int:
        """

        :return: The rumble in the range 0 to 65535
        """
        return self.rumble.read_u16()

    def inverted_y_axis(self) -> bool:
        """
        Tell if the Y-Axis is inverted for player joystick inputs.
        :return: True if the Y-Axis should be inverted for flight controls.
        """
        return bool(self.invert_y.value())
