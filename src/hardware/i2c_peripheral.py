# Peripheral Controller for the Raspberry PI Pico
# https://forums.raspberrypi.com/viewtopic.php?t=302978#p1823668
#
# version: 3.4.0; MicroPython v1.20.0 on 2023-04-26 port: rp2
from machine import mem32


class I2cPeripheral:
    I2C0_BASE = 0x40044000
    I2C1_BASE = 0x40048000
    IO_BANK0_BASE = 0x40014000

    mem_rw = 0x0000
    mem_xor = 0x1000
    mem_set = 0x2000
    mem_clr = 0x3000

    IC_CON = 0
    IC_TAR = 4
    IC_SAR = 8
    IC_DATA_CMD = 0x10
    IC_RAW_INTR_STAT = 0x34
    IC_RX_TL = 0x38
    IC_TX_TL = 0x3C
    IC_CLR_INTR = 0x40
    IC_CLR_RD_REQ = 0x50
    IC_CLR_TX_ABRT = 0x54
    IC_ENABLE = 0x6c
    IC_STATUS = 0x70

    def write_reg(self, reg, data, method=0):
        mem32[self.i2c_base | method | reg] = data

    def set_reg(self, reg, data):
        self.write_reg(reg, data, method=self.mem_set)

    def clr_reg(self, reg, data):
        self.write_reg(reg, data, method=self.mem_clr)

    def __init__(self, i2c_id=0, sda=0, scl=1, address=0x41):
        self.scl = scl
        self.sda = sda
        self.slaveAddress = address
        self.i2c_ID = i2c_id
        if self.i2c_ID == 0:
            self.i2c_base = self.I2C0_BASE
        else:
            self.i2c_base = self.I2C1_BASE

        # 1 Disable DW_apb_i2c
        self.clr_reg(self.IC_ENABLE, 1)
        # 2 set slave address
        # clr bit 0 to 9
        # set slave address
        self.clr_reg(self.IC_SAR, 0x1ff)
        self.set_reg(self.IC_SAR, self.slaveAddress & 0x1ff)
        # 3 write IC_CON  7 bit, enable in slave-only
        self.clr_reg(self.IC_CON, 0b01001001)
        # set SDA PIN
        mem32[self.IO_BANK0_BASE | self.mem_clr | (4 + 8 * self.sda)] = 0x1f
        mem32[self.IO_BANK0_BASE | self.mem_set | (4 + 8 * self.sda)] = 3
        # set SLA PIN
        mem32[self.IO_BANK0_BASE | self.mem_clr | (4 + 8 * self.scl)] = 0x1f
        mem32[self.IO_BANK0_BASE | self.mem_set | (4 + 8 * self.scl)] = 3
        # 4 enable i2c
        self.set_reg(self.IC_ENABLE, 1)

    def any_read(self):
        """ Is there any available data to read. """
        status = mem32[self.i2c_base | self.IC_RAW_INTR_STAT] & 0x20
        if status:
            return True
        return False

    def put(self, data):
        """
        Write data to the I2c line
        :param data:
        :return:
        """
        packet = 0x0
        if isinstance(data, str):
            packet = bytearray()
            data.encode('utf-8')

        elif isinstance(data, bytearray):
            packet = data

        else:
            print(f'Could not send data packet over I2C: {data}')
            return

        # reset flag
        self.clr_reg(self.IC_CLR_TX_ABRT, 1)
        status = mem32[self.i2c_base | self.IC_CLR_RD_REQ]
        mem32[self.i2c_base | self.IC_DATA_CMD] = data & 0xff

    def any(self):
        """
        Is there any available data to read?
        :return:
        """
        # get IC_STATUS
        status = mem32[self.i2c_base | self.IC_STATUS]
        # check RFNE receive fifio not empty
        if status & 8:
            return True
        return False

    def get(self):
        """
        Get the data that was put to this device
        :return:
        """
        while not self.any():
            pass
        return mem32[self.i2c_base | self.IC_DATA_CMD] & 0xff
