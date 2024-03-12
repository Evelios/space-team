from ..display.mileage import Mileage
import time


def main():
    print("Testing the mileage display by incrementing the counter.")

    mileage = Mileage(pin=2)

    while True:
        mileage.increment()
        time.sleep(0.5)
