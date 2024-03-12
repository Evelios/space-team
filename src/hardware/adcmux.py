from machine import Pin


class AdcMux:
    SEL0_MASK = 0x0001
    SEL1_MASK = 0x0010
    SEL2_MASK = 0x0100
    SEL3_MASK = 0x1000

    def __init__(self, ain: int, sel0: int, sel1: int, sel2: int, sel3: int):
        self.ain = Pin(ain)
        self.sel0 = Pin(sel0)
        self.sel1 = Pin(sel1)
        self.sel2 = Pin(sel2)
        self.sel3 = Pin(sel3)
        # self.enable = Pin(e)
        self._reset()

    def read(self, pin: int) -> int:
        """
        Read the value from the ADC multiplexer. If you give a pin value out of
        range the function fails silently and returns 0 (Low)

        :param pin: The number of the pin in reference to the ADC. This value
            should be between 0 and 7 (8 bit ADC)
        :return: The value of the pin 0 (Low) or 1 (High)
        """

        # If the pin value is out of range return 0 and fail silently
        if 0 < pin >= 8:
            return 0

        self._select_pin(pin)
        return self.ain.value()

    def write(self, pin: int, value: int) -> None:
        """
        Write the value to the ADC multiplexer. If you give a pin value out of
        range the function fails silently and returns.

        :param pin: The number of the pin in reference to the ADC. This value
            should be between 0 and 7 (8 bit ADC)
        :param value:
        :return:
        """
        # If the pin value is out of range return
        if 0 < pin >= 8:
            return

        self._select_pin(pin)
        self.ain.value(value)

    def _select_pin(self, pin: int) -> None:
        # Set the select pins based off the select masks to get access to the
        # analog read pin
        self.sel0.value(pin & AdcMux.SEL0_MASK)
        self.sel1.value(pin & AdcMux.SEL1_MASK)
        self.sel2.value(pin & AdcMux.SEL2_MASK)
        self.sel3.value(pin & AdcMux.SEL3_MASK)

    def _reset(self):
        self.sel0.off()
        self.sel1.off()
        self.sel2.off()
        self.sel3.off()
        # self.enable.off()
