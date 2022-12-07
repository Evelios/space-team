class GeneratorState:
    OVERDRIVE = 0
    ON = 1
    OFF = 2


class Power:
    """
    Power panel
    """

    def __init__(self):
        self.state = GeneratorState.ON
