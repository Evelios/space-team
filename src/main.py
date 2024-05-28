# from tests import lcd_basic, ping_pong, i2c_pullup, vibration_motor, stability_display
from spaceteam import SpaceTeam

print(f"""
      Running Space Team
      ------------------
      """)

if __name__ == "__main__":
    app = SpaceTeam()
    app.run()
