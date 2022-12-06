from enum import Enum, auto

class GeneratorState(Enum):
    OVERDRIVE = auto()
    ON = auto()
    OFF = auto()

class Power:
    """
    Power panel
    """
    def __init__(self):
        self.state = GeneratorState.ON
