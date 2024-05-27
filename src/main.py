# from tests import lcd_basic, ping_pong, i2c_pullup, vibration_motor
from tests import stability_display

print(f"""
      Running Space Team
      ------------------
      """)


def main():
    stability_display.main()


def all_tests():
    # vibration_motor.main()
    # i2c_pullup.main()
    # lcd_basic.main()
    # ping_pong.main()
    pass


if __name__ == "__main__":
    main()
