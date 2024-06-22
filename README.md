# Space Team

This is what Space Team is all about!

## Raspberry Pi Pico

The Raspberry Pi Pico is the brains of Space Team. It is the microcontroller that handles all the input devices and
send messages back to the lights and displays.

### Flashing the Pico Software

When you have a new pico, or a pico that was just flashed with [flash_nuke.uf2](firmware/flash_nuke.uf2), you need to
install the MicroPython firmware onto the pico. You just need to hold the boot select pin on the pico and plug in the
USB Micro. This should open a window explorer on the desktop. All you have to do to upload the base firmware to the pico
is to copy [firmware/rp2-pico-20230426-v1.20.0.uf2](firmware/rp2-pico-20230426-v1.20.0.uf2) onto the pico by bringing it
into the file window. The pico should restart and the file window should close. This is how you know that the firmware
updated.

For easy reference, the important files for flashing the Pico with the Space Team software are

* Space Team MicroPython Source Code
    * [src/](src)
* MicroPython / Raspberry Pi Pico Firmware
    * [firmware/rp2-pico-20230426-v1.20.0.uf2](firmware/rp2-pico-20230426-v1.20.0.uf2)
* Pico Hardware Reset
    * [firmware/flash_nuke.uf2](firmware/flash_nuke.uf2)

### Interacting with the Raspberry Pi Pico

```sh
# Install mpremote software
pip install mpremote

# Install required typing modules to allow for static type checking in code
python -m mpremote mip install github:josverl/micropython-stubs/mip/typing.mpy
python -m mpremote mip install github:josverl/micropython-stubs/mip/typing_extensions.mpy

# Connect to local devices
python -m mpremote
```

## Generating Documentation

Install the `sphinx` tool and run the following command from the root directory.

* [Example Sphinx/Micropython Project](https://github.com/russhughes/st7789py_mpy)

```shell
# Install the documentation generation tools
pip install sphinx sphinx_rtd_theme
pip install -I micropython-stm32-stubs

# Generate the codes module docstring information
sphinx-apidoc -o docs src

# Generate the documentation
sphinx-build -M html src _build

# This is also handled by the makefiles at the project root
make html
```

## Development

* Latest Pico Firmware: https://micropython.org/download/rp2-pico/
* Pico Micropython Documentation: https://docs.micropython.org/en/latest/rp2/quickref.html
* Getting Micropython Working on Teensy
  3.X: https://learn.sparkfun.com/tutorials/how-to-load-micropython-on-a-microcontroller-board/teensy-3x

## Libraries

* MCP2017 Digital IO Expander: https://github.com/sensorberg/MCP23017-python