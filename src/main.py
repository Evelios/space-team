# from tests import lcd_basic, ping_pong, i2c_pullup, vibration_motor, stability_display
from spaceteam import SpaceTeam


def main():
    """
    Run the main application.
    """
    print(
        f"""
        Running Space Team
        ------------------
        """)

    app = SpaceTeam()
    app.run()


if __name__ == "__main__":
    main()
