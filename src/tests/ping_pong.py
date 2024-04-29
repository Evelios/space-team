# Ping-pong test script for the pi pico I2C peripheral tests.
#
# Notes:
#   In order to run this script, the pi pico has to be flashed with new firmware to allow for the functionality of I2C
#   slave module capability. How to use the Pico as an I2C slave module:
#   -  https://github.com/vmilea/pico_i2c_slave
#
# 4.3.10.1.3. Slave-Receiver Operation for a Single Byte
# When another I2C master device on the bus addresses the DW_apb_i2c and is sending data, the DW_apb_i2c acts as a
# slave-receiver and the following steps occur:
# 1. The other I2C master device initiates an I2C transfer with an address that matches the DW_apb_i2c’s slave
# address in the IC_SAR register.
# 2. The DW_apb_i2c acknowledges the sent address and recognizes the direction of the transfer to indicate that the
# DW_apb_i2c is acting as a slave-receiver.
# 3. DW_apb_i2c receives the transmitted byte and places it in the receive buffer.
#  NOTE
# If the Rx FIFO is completely filled with data when a byte is pushed, then the DW_apb_i2c slave holds the I2C SCL line
# low until the Rx FIFO has some space, and then continues with the next read request.
# 1. DW_apb_i2c asserts the RX_FULL interrupt IC_RAW_INTR_STAT.RX_FULL. If the RX_FULL interrupt has been
# masked, due to setting IC_INTR_MASK.M_RX_FULL register to zero or setting IC_TX_TL to a value larger than zero,
# then it is recommended that a timing routine (described in Section 4.3.10.1.2) be implemented for periodic reads
# of the IC_STATUS register. Reads of the IC_STATUS register, with bit 3 (RFNE) set at one, must then be treated by
# software as the equivalent of the RX_FULL interrupt being asserted.
# 2. Software may read the byte from the IC_DATA_CMD register (bits 7:0).
# 3. The other master device may hold the I2C bus by issuing a RESTART condition, or release the bus by issuing a
# STOP condition.
from hardware.i2c_peripheral import I2cPeripheral


def get_response(req: str = ""):
    if req.upper() == "PONG":
        return "PING"
    else:
        return "PONG"


def main():
    sda = 4
    scl = 5
    address = 84
    peripheral = I2cPeripheral(0, sda, scl, address)
    request = ""

    print("Pico I2C Peripheral")
    print(f"Address: {address}, 0x{address:02x}")
    print(f"SDA: Pin {sda}, SCL: Pin {scl}")

    try:
        while True:
            if peripheral.any():
                request = peripheral.get()
                print(f"Request: {request}")
            if peripheral.any_read():
                response = get_response(request)
                peripheral.put(response)
                print(f"Response: {response}")

    except KeyboardInterrupt:
        pass
