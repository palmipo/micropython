from hd44780io import HD44780IO
from pcf8574t import PCF8574T
import time

DB7 = 7
DB6 = 6
DB5 = 5
DB4 = 4
BACKLIGHT = 3
EN = 2
RW_ = 1
RS = 0

class LCD2004(HD44780IO):

    def __init__(self, adresse, i2c):
        super().__init__()
        self.backlight = 0

        self.gpio = PCF8574T(adresse, i2c)
        self.gpio.setIODIR(0)

    def setBackLight(self, value):
#         print("setBackLight("+hex(value)+")")
        self.backlight = (value & 0x01) << BACKLIGHT
        self.gpio.setOLAT(self.backlight)

    def writeCmd(self, cmd):
#         print("writeCmd("+hex(cmd)+")")
        self.enableBit((((cmd & 0x80) >> 7) << DB7) | (((cmd & 0x40) >> 6) << DB6) | (((cmd & 0x20) >> 5) << DB5) | (((cmd & 0x10) >> 4) << DB4))
        self.enableBit((((cmd & 0x08) >> 3) << DB7) | (((cmd & 0x04) >> 2) << DB6) | (((cmd & 0x02) >> 1) << DB5) | (((cmd & 0x01) >> 0) << DB4))

    def writeData(self, cmd):
#         print("writeData("+hex(cmd)+")")
        self.enableBit((((cmd & 0x80) >> 7) << DB7) | (((cmd & 0x40) >> 6) << DB6) | (((cmd & 0x20) >> 5) << DB5) | (((cmd & 0x10) >> 4) << DB4) | (1 << RS))
        self.enableBit((((cmd & 0x08) >> 3) << DB7) | (((cmd & 0x04) >> 2) << DB6) | (((cmd & 0x02) >> 1) << DB5) | (((cmd & 0x01) >> 0) << DB4) | (1 << RS))

    def enableBit(self, data):
#         print("enableBit("+hex(data)+")")
        self.gpio.setOLAT(self.backlight | data)
        time.sleep_ms(1)
        self.gpio.setOLAT(self.backlight | data | (1 << EN))
        time.sleep_ms(2)
        self.gpio.setOLAT(self.backlight | data)
        time.sleep_ms(1)

    def write(self, data, rs, rw_, en):
        cmd = self.backlight | (((data & 0x80) >> 7) << DB7) | (((data & 0x40) >> 6) << DB6) | (((data & 0x20) >> 5) << DB5) | (((data & 0x10) >> 4) << DB4) | ((rw_ & 0x01) << RW_) | ((rs & 0x01) << RS)
 
        self.gpio.setOLAT(cmd)
        time.sleep_ms(1)

        self.gpio.setOLAT(cmd | (1 << EN))
        time.sleep_ms(2)

        self.gpio.setOLAT(cmd)
        time.sleep_ms(1)

    def bitMode(self):
        return 0

    def nLine(self):
        return 1

    def fontMode(self):
        return 0

