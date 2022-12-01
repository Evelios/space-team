import utime
from machine import Pin

LCD_RW_READ = 1
LCD_RW_WRITE = 0

ENABLE_ON = 1
ENABLE_OFF = 0

RS_DATA_SELECT = 1
RS_INSTRUCTION_SELECT = 0

MODE_8_BITS = 1  # MODE_8_BITS: interfaces with LCD with 8 data bits at a time.
MODE_4_BITS = 0  # MODE_4_BITS: interfaces with LCD with two nibbles of 4 bits at a time.

DISPLAY_LINES_1 = 0
DISPLAY_LINES_2 = 1


class BitMask:
    """
    Bit masks for working with 8 bit values
    """
    BIT7 = 0b10000000
    BIT6 = 0b01000000
    BIT5 = 0b00100000
    BIT4 = 0b00010000
    BIT3 = 0b00001000
    BIT2 = 0b00000100
    BIT1 = 0b00000010
    BIT0 = 0b00000001


class Characters:


    Backslash = [
        0b00000,
        0b10000,
        0b01000,
        0b00100,
        0b00010,
        0b00001,
        0b00000,
        0b00000]


class LcdCommands:
    """
    8-bit Command codes needed to operate the LCD
    """
    CLEAR = 0b00000001
    HOME = 0b00000010
    CURSOR_BACKWARD = 0b00000100
    CURSOR_FORWARD = 0b00000110
    DISPLAY_OFF = 0b00001000
    DISPLAY_ON = 0b00001100
    DISPLAY_BLINK_OFF = 0b00001100
    DISPLAY_BLINK_ON = 0b00001111
    CURSOR_LEFT = 0b00010000
    CURSOR_RIGHT = 0b00010100
    SHIFT_TEXT_LEFT = 0b00011000
    SHIFT_TEXT_RIGHT = 0b00011100
    FUNCTION_SET = 0b00010100
    SET_CGRAM = 0b00100000
    SET_DDRAM = 0b01000000
    FIRST_LINE = 0b10000000
    SECOND_LINE = 0b11000000

    @staticmethod
    def entry_mode(increment_cursor=False, shift=False) -> int:
        """
        Sets the entry mode for the LCD
        :param increment_cursor: I/D Parameter
        :param shift: True=shift left, False=shift right
        :return: The bit command to send to the LCD
        """
        return 0b00000100 | increment_cursor >> 1 | shift

    @staticmethod
    def display(on=True, cursor=False, blink=False) -> int:
        """
        Sets the display properties for the LCD
        :param on: Either turns the display ON or OFF
        :param cursor: Turn the cursor ON or OFF
        :param blink: Determines if the cursor should blink or not
        :return: The bit command to send to the LCD
        """
        return 0b00001000 | on >> 3 | cursor >> 2 | blink

    @staticmethod
    def function_set(data_length=MODE_4_BITS, display_lines=DISPLAY_LINES_1, character_font=False) -> int:
        """
        Sets the display properties for the LCD
        :param data_length:
            Number of pins used for communication.
            0 = 4 bit/pin mode
            1 = 8 bit/pin mode
        :param display_lines: 0 = 1 line, 1 = 2 lines
        :param character_font:
        :return: The bit command to send to the LCD
        """
        return 0b00100000 | data_length >> 4 | display_lines >> 3 | character_font >> 2


# LCD class for displaying to a parallel interface LDC
class Lcd:
    def __init__(self, rs, e, d4, d5, d6, d7):
        self.rs = Pin(rs, Pin.OUT)
        self.e = Pin(e, Pin.OUT)
        self.d4 = Pin(d4, Pin.OUT)
        self.d5 = Pin(d5, Pin.OUT)
        self.d6 = Pin(d6, Pin.OUT)
        self.d7 = Pin(d7, Pin.OUT)
        self.__setup()

    def entry_mode(self, increment_cursor=False, shift=False):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.entry_mode(increment_cursor, shift), MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def display(self, on=True, cursor=False, blink=False):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.display(on, cursor, blink), MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def function_set(self, data_length=MODE_4_BITS, display_lines=DISPLAY_LINES_1, character_font=False):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.function_set(data_length, display_lines, character_font), MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def cursor_home(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.HOME, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)
        self.__delay()

    def first_line(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.FIRST_LINE, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)
        self.__delay()

    def second_line(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.SECOND_LINE, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)
        self.__delay()

    def cursor_move_forward(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.CURSOR_FORWARD, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def cursor_move_back(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.CURSOR_FORWARD, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def clear(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.CLEAR, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)
        self.__delay()

    def move_cursor_right(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.CURSOR_RIGHT, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def move_cursor_left(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.CURSOR_LEFT, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def display_blink_on(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.DISPLAY_BLINK_ON, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def display_blink_off(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.DISPLAY_BLINK_ON, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def display_shift_text_right(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.SHIFT_TEXT_RIGHT, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def display_shift_text_left(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.SHIFT_TEXT_RIGHT, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def display_off(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.DISPLAY_OFF, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def display_on(self):
        self.rs.value(RS_INSTRUCTION_SELECT)
        self.__write_char(LcdCommands.DISPLAY_ON, MODE_8_BITS)
        self.rs.value(RS_DATA_SELECT)

    def create_character(self, character, position=0):
        """
        Create a custom character and store it on the LCD.
        There can only be 8 custom characters loaded onto each LCD.

        :param character: The array of 8 columns of bitfields of length 5
        :param position: The position (0 to 7) in the buffer to save the custom character.
        """
        if 0 <= position < 8:
            return

        self.rs.value(RS_INSTRUCTION_SELECT)

        # Enable the character writing at the given position
        command = LcdCommands.SET_CGRAM | position << 3
        self.__write_char(byte, MODE_8_BITS)

        # Write the character to the display
        for byte in character:
            self.__write_char(byte, MODE_8_BITS)

        self.rs.value(RS_DATA_SELECT)

    def move_to(self, line: int, column: int):
        if line == 1:
            self.second_line()
        else:
            self.first_line()

        for _ in range(0, column):
            self.move_cursor_right()

    def __write_char(self, char, mode):
        if mode is MODE_8_BITS:
            self.d4.value((char & BitMask.BIT4) >> 4)
            self.d5.value((char & BitMask.BIT5) >> 5)
            self.d6.value((char & BitMask.BIT6) >> 6)
            self.d7.value((char & BitMask.BIT7) >> 7)
            self.__toggle_enable()

        self.d4.value((char & BitMask.BIT0) >> 0)
        self.d5.value((char & BitMask.BIT1) >> 1)
        self.d6.value((char & BitMask.BIT2) >> 2)
        self.d7.value((char & BitMask.BIT3) >> 3)
        self.__toggle_enable()

    def write(self, message):
        for char in message:
            self.__write_char(ord(char), MODE_8_BITS)
            self.__delay()

    def __toggle_enable(self):
        self.e.value(ENABLE_ON)
        self.__short_delay()
        self.e.value(ENABLE_OFF)
        self.__short_delay()

    def __setup(self):
        instructions_4_bit = [
            0b0011,  # 8 bit
            0b0011,  # 8 bit
            0b0011,  # 8 bit
            0b0010  # 4 bit
        ]

        instructions_8_bit = [
            LcdCommands.function_set(
                data_length=MODE_4_BITS,
                display_lines=DISPLAY_LINES_2),

            LcdCommands.DISPLAY_ON,

            LcdCommands.entry_mode(increment_cursor=True),

            LcdCommands.CLEAR
        ]

        self.rs.value(RS_INSTRUCTION_SELECT)

        for instruction in instructions_4_bit:
            self.__write_char(instruction, MODE_4_BITS)

        for instruction in instructions_8_bit:
            self.__write_char(instruction, MODE_8_BITS)

        self.rs.value(RS_DATA_SELECT)

    # ---- Static Methods ----

    @staticmethod
    def __short_delay():
        """ Pause for 40 us """
        utime.sleep_us(40)

    @staticmethod
    def __delay():
        """ Pause for 2 ms """
        utime.sleep_ms(2)

    @staticmethod
    def __long_delay():
        """ Pause for 2 ms """
        utime.sleep(0.3)
