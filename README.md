# Space Team

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