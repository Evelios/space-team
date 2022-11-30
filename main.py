from lcd import Lcd

lcd = Lcd(rs=16, e=17, d4=18, d5=19, d6=20, d7=21)

lcd.move_to(0, 1)
lcd.write('Hi, Human.')

lcd.move_to(1, 1)
lcd.write('Hello, Pico!')
