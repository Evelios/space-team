from enum import Enum, auto


class Switch(Enum):
    ON = auto()
    OFF = auto()


class Button(Enum):
    PRESSED = auto()
    RELEASED = auto()
