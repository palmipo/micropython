from hd44780io import HD44780IO
import time

BACKLIGHT = 0
DB7 = 1
DB6 = 2
DB5 = 3
DB4 = 4
EN = 5
RW_ = 6
RS = 7

class ADA772(HD44780IO):

    def __init__(self, pia1, pia2):
        super().__init__()
        self.pia = pia1
        self.switchs = pia2

    def setBackLight(self, value):
        self.backlight = value & 0x01
        self.pia.setOutput(self.backlight << BACKLIGHT)
        self.switchs.setOutput(0)

    def writeCmd(self, cmd):
        self.enableBit((self.backlight & 0x01) | ((cmd & 0x80) << DB7) | ((cmd & 0x40) << DB6) | ((cmd & 0x20) << DB5) | ((cmd & 0x10) << DB4))
        self.enableBit((self.backlight & 0x01) | ((cmd & 0x08) << DB7) | ((cmd & 0x04) << DB6) | ((cmd & 0x02) << DB5) | ((cmd & 0x01) << DB4))

    def writeData(self, cmd):
        self.enableBit((self.backlight & 0x01) | ((cmd & 0x80) << DB7) | ((cmd & 0x40) << DB6) | ((cmd & 0x20) << DB5) | ((cmd & 0x10) << DB4) | (1 << RS))
        self.enableBit((self.backlight & 0x01) | ((cmd & 0x08) << DB7) | ((cmd & 0x04) << DB6) | ((cmd & 0x02) << DB5) | ((cmd & 0x01) << DB4) | (1 << RS))

    def enableBit(self, data):
        self.pia.setOutput(data)
        time.sleep_ms(1)
        self.pia.setOutput(data | (1 << EN))
        time.sleep_ms(2)
        self.pia.setOutput(data)
        time.sleep_ms(1)

        busy = self.isBusy()
        while busy:
            busy = self.isBusy()

    def isBusy(self):
        octet = self.readCmd()
        if (octet & 0x80) != 0:
            return True
        else:
            return False

    def readData(self):
        self.pia.setOutput((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << RS) | (1 << EN))
        time.sleep_ms(1)
        octet = self.pia.getInput()
        data = bytearray(1)
        data[0] = ((octet & (1 << DB7)) >> DB7) << 7
        data[0] |= ((octet & (1 << DB6)) >> DB6) << 6
        data[0] |= ((octet & (1 << DB5)) >> DB5) << 5
        data[0] |= ((octet & (1 << DB4)) >> DB4) << 4
        self.pia.setOutput((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << RS))
        time.sleep_ms(2)
        self.pia.setOutput((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << RS) | (1 << EN))
        time.sleep_ms(1)
        octet = self.pia.getInput()
        data[0] |= ((octet & (1 << DB7)) >> DB7) << 3
        data[0] |= ((octet & (1 << DB6)) >> DB6) << 2
        data[0] |= ((octet & (1 << DB5)) >> DB5) << 1
        data[0] |= ((octet & (1 << DB4)) >> DB4)
        self.pia.setOutput(self.backlight << BACKLIGHT)
        return data[0]

    def readCmd(self):
        self.pia.setOutput((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << EN))
        time.sleep_ms(1)

        octet = self.pia.getInput() # type byte
        data = bytearray(1)
        data[0] = ((octet & (1 << DB7)) >> DB7) << 7
        data[0] |= ((octet & (1 << DB6)) >> DB6) << 6
        data[0] |= ((octet & (1 << DB5)) >> DB5) << 5
        data[0] |= ((octet & (1 << DB4)) >> DB4) << 4

        self.pia.setOutput((self.backlight << BACKLIGHT) | (1 << RW_))
        time.sleep_ms(2)
        
        self.pia.setOutput((self.backlight << BACKLIGHT) | (1 << RW_) | (1 << EN))
        time.sleep_ms(1)
        
        octet = self.pia.getInput()
        data[0] |= ((octet & (1 << DB7)) >> DB7) << 3
        data[0] |= ((octet & (1 << DB6)) >> DB6) << 2
        data[0] |= ((octet & (1 << DB5)) >> DB5) << 1
        data[0] |= ((octet & (1 << DB4)) >> DB4)
        
        self.pia.setOutput(self.backlight << BACKLIGHT)
        return data[0]

    def write(self, data, rs, rw_, en):
        cmd = (((data & 0x80) >> 7) << DB7) | (((data & 0x40) >> 6) << DB6) | (((data & 0x20) >> 5) << DB5) | (((data & 0x10) >> 4) << DB4) | ((rw_ & 0x01) << RW_) | ((rs & 0x01) << RS)
        self.enableBit(cmd)
#         self.pia.setOutput(cmd)
#         time.sleep_ms(1)
#         self.pia.setOutput(cmd | (1 << EN))
#         time.sleep_ms(2)
#         self.pia.setOutput(cmd)
#         time.sleep_ms(1)

    def bitMode(self):
        return 0

    def nLine(self):
        return 1

