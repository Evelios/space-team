# Testing the functionality of the rotary encoder
# I2C Connected to LCD display with 5v from USB. There are two 5k resistors pulling up the SCL(1) and SDA(0) pins.

from machine import Pin, I2C
import gc
import time

from display.lcd_pico import I2cLcd


def main():
    print("I2C - LCD test start")
    # open I2C port
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
        print("No i2c device !")
    else:
        print('i2c devices found:', len(devices))

    for device in devices:
        print("Decimal address: ", device, " | Hexa address: ", hex(device))

    # now create LCD object with, hopefully, the only address found
    lcd = I2cLcd(i2c, devices[0], 2, 16)

    # Test
    lcd.backlight_on()

    # build special character
    special_char = bytearray([0x4, 0xe, 0x1f, 0x4, 0x4, 0x4, 0x4, 0x4])
    time.sleep(1)
    lcd.clear()
    lcd.custom_char(0x0, special_char)
    lcd.putstr("Hello World \n")

    for repeat in range(2):
        for x in range(20):
            lcd.move_to(x, 1)
            lcd.putchar(chr(0))
            time.sleep(0.2)
            lcd.move_to(x, 1)
            lcd.putchar(" ")

    time.sleep(1)
    lcd.blink_cursor_off()
    lcd.hide_cursor()
    lcd.move_to(10, 2)

    for x in range(ord('A'), ord('Z')):
        lcd.putchar_no_move(chr(x))
        lcd.move_cursor_left()
        time.sleep(0.3)

    lcd.move_to(10, 3)
    lcd.putchar_no_move('*')
    lcd.show_cursor()

    for x in range(10):
        lcd.move_cursor_left()
        time.sleep(0.3)

    for x in range(10):
        lcd.move_cursor_right()
        time.sleep(0.3)

    time.sleep(0.3)
    lcd.backlight_off()
    print("I2C - LCD test end")
    lcd.display_off()
    lcd.backlight_off()

    gc.collect()
    print(gc.mem_free())
    print(gc.mem_alloc())
