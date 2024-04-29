# Testing the functionality of the rotary encoder
# I2C Connected to LCD display with 5v from USB. There are two 5k resistors pulling up the SCL(1) and SDA(0) pins.

from machine import Pin, I2C
import gc
import time

from display.lcd_pico import I2cLcd


def main():
    print('I2C - LCD test start')
    # open I2C port
    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
    peripheral_address = 84
    lcd_address = 39  # 63

    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
        print('No I2C devices found !')
        print('Ending Test')
        return
    else:
        print('I2C devices found:', len(devices))

    for device in devices:
        print(f'Decimal address: {device} | Hexa address: {hex(device)})')

    # if lcd_address not in devices or peripheral_address not in devices:
    #     print('Not all I2C Devices are present!')
    #     print('Ending Test')
    #     return

    # now create LCD object with
    lcd = I2cLcd(i2c, lcd_address, 2, 16)
    lcd.backlight_on()

    # Devices found
    for device in devices:
        lcd.clear()
        lcd.putstr(f'Addr: {device}, {hex(device)}')
        time.sleep(2)

    # Write To LCD Screen
    print('LCD Hello World')
    lcd.clear()
    lcd.putstr(f'Hello World')

    time.sleep(2)
    print('Ping Pong Test Started')
    lcd.clear()
    lcd.putstr('Ping Pong\n')
    time.sleep(1)

    # Ping the I2C Peripheral
    print(f'Pinging Peripheral with "Ping"')
    i2c.writeto(peripheral_address, 'Ping')
    response = i2c.readfrom(peripheral_address, 4)
    lcd.clear()
    print(f'Response: {response}')
    if response:
        lcd.putstr(response)
    else:
        lcd.putstr("No PING")

    time.sleep(2)

    lcd.clear()
    print(f'Pinging Peripheral with "Pong"')
    i2c.writeto(peripheral_address, 'Pong')
    response = i2c.readfrom(peripheral_address, 4).decode('utf-8')
    print(f'Response: {response}')
    if response:
        lcd.putstr(response)
    else:
        lcd.putstr("No PONG")

    time.sleep(2)

    # End Test
    print(f'Test Ended')
    lcd.clear()
    lcd.putstr('Goodbye World\n')
