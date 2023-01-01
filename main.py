import utime

import machine
from machine import I2C
from joystick import Joystick
from stability import Stability
from heading import Heading

# joystick = Joystick(27, 28)

I2C_ADDR = 39

print("Running test_main")

heading = Heading(din=28)

heading.display()




# i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
# stability = Stability(i2c, I2C_ADDR)
#
# stability.display()
#
# while True:
#     for i in range(100):
#         utime.sleep_ms(1)
#         joystick.update()
#     print(joystick.x)
#     stability.set_position(joystick.y)
