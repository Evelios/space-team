import time

from controller.stabilizer import Stabilizer

stabilizer = Stabilizer(3,2, 4, 5)

while (True):
    stabilizer.update()
    time.sleep_ms(100)
