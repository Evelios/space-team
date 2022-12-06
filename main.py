from display.lcd import Lcd
from sensor.button import Button

lcd = Lcd(rs=16, e=17, d4=18, d5=19, d6=20, d7=21)
lcd.display(on=True, cursor=True, blink=True)

lcd.move_to(0, 1)
lcd.write('Hi, Human.')

lcd.move_to(1, 1)
lcd.write('Hello, Pico!')

button = Button(2)

while True:
    pass
