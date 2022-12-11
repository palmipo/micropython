from hd44780io import HD44780IO
from pcf8574t import PCF8574T
from pia_pcf8574 import PIA_PCF8574
import time


class LCD2004(HD44780IO):

    def __init__(self, adresse, i2c):
        super().__init__()
        self.backlight = 0
        self.DB7 = 7
        self.DB6 = 6
        self.DB5 = 5
        self.DB4 = 4
        self.BACKLIGHT = 3
        self.EN = 2
        self.RW_ = 1
        self.RS = 0

        self.gpio = PCF8574T(adresse, i2c)
        self.gpio.setIODIR(0)

        self.pia = PIA_PCF8574(self.gpio)

    def setBackLight(self, value):
#         print("setBackLight("+hex(value)+")")
        self.backlight = (value & 0x01) << self.BACKLIGHT
        self.pia.setOutput(self.backlight)

    def writeCmd(self, cmd):
#         print("writeCmd("+hex(cmd)+")")
        self.enableBit((((cmd & 0x80) >> 7) << self.DB7) | (((cmd & 0x40) >> 6) << self.DB6) | (((cmd & 0x20) >> 5) << self.DB5) | (((cmd & 0x10) >> 4) << self.DB4))
        self.enableBit((((cmd & 0x08) >> 3) << self.DB7) | (((cmd & 0x04) >> 2) << self.DB6) | (((cmd & 0x02) >> 1) << self.DB5) | (((cmd & 0x01) >> 0) << self.DB4))

    def writeData(self, cmd):
#         print("writeData("+hex(cmd)+")")
        self.enableBit((((cmd & 0x80) >> 7) << self.DB7) | (((cmd & 0x40) >> 6) << self.DB6) | (((cmd & 0x20) >> 5) << self.DB5) | (((cmd & 0x10) >> 4) << self.DB4) | (1 << self.RS))
        self.enableBit((((cmd & 0x08) >> 3) << self.DB7) | (((cmd & 0x04) >> 2) << self.DB6) | (((cmd & 0x02) >> 1) << self.DB5) | (((cmd & 0x01) >> 0) << self.DB4) | (1 << self.RS))

    def enableBit(self, data):
#         print("enableBit("+hex(data)+")")
        self.pia.setOutput(self.backlight | data)
        time.sleep_ms(1)
        self.pia.setOutput(self.backlight | data | (1 << self.EN))
        time.sleep_ms(2)
        self.pia.setOutput(self.backlight | data)
        time.sleep_ms(1)

    def write(self, data, rs, rw_, en):
        cmd = self.backlight | (((data & 0x80) >> 7) << self.DB7) | (((data & 0x40) >> 6) << self.DB6) | (((data & 0x20) >> 5) << self.DB5) | (((data & 0x10) >> 4) << self.DB4) | ((rw_ & 0x01) << self.RW_) | ((rs & 0x01) << self.RS)
 
        self.pia.setOutput(cmd)
        time.sleep_ms(1)

        self.pia.setOutput(cmd | (1 << self.EN))
        time.sleep_ms(2)

        self.pia.setOutput(cmd)
        time.sleep_ms(1)

    def bitMode(self):
        return 0

    def nLine(self):
        return 1

    def fontMode(self):
        return 0

