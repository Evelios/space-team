# Testing the functionality of the rotary encoder
from sensor.rotary_encoder import RotaryEncoder

# ---- Variables ----

encoder = RotaryEncoder(5, 4, 2, 3)


# ---- Events ----


def on_change():
    print(f'Encoder Position: "{encoder.position}"')


# ---- Initialization ----

def setup():
    encoder.on_change(on_change)


def loop():
    encoder.update()
    print(f'Looping... Encoder Position: "{encoder.position}"')


def main():
    print(
        f"""
        Running tests on the rotary encoder.
        Test will show each value of the encoder when it changes.
        Current encoder reading is: "{encoder.position}"
        """)

    setup()
    while True:
        loop()
