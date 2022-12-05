from machine import Pin


class Stabilizer:
    """
    Stabilizer panel
    """

    stability = 0
    """Stability of this device. Range -1 -> 1"""

    rotary_encoder = None
    """stabilizer_input"""

    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.rotary_encoder = (p1, p2, p3, p4, p5, p6)
