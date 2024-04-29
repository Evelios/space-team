from tests import stability_display, lcd_basic, ping_pong, i2c_pullup

print(f"""
      Running Space Team
      ------------------
      """)


def main():
    i2c_pullup.main()


def all_tests():
    lcd_basic.main()
    stability_display.main()
    ping_pong.main()


if __name__ == "__main__":
    main()
