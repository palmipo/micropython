from device.spi.st7789 import ST7789
from neopixel import NeoPixel
from machine import Pin
from master.pia.piapico import PiaOutputPico
from master.pwm.pwmpico import PwmPico
import time

class Lcd_1inch14(ST7789):
    def __init__(self, num, dc, rst, spi, bl):
        self.DC_PIN = dc
        self.RST_PIN = rst
        self.spi = spi
        self.BL_PIN = bl
        self.BL_PIN.setFrequency(1000)
        self.BL_PIN.setDuty(50)
        self.num = num
        self.width = 135
        self.height = 240

        super().__init__()

    def setLcdBlackLight(self, lev):#0-100
        self.BL_PIN.setDuty(lev % 100)

    def write_cmd(self, cmd):
        self.DC_PIN.set(0)
        data = bytearray(1)
        data[0] = cmd
        self.spi.send(self.num, data)
        
    def write_data(self, val):
        self.DC_PIN.set(1)
        data = bytearray(1)
        data[0] = val
        self.spi.send(self.num, data)

    def write_buffer(self, buf):
        self.DC_PIN.set(1)
        for i in range(0,len(buf),4096):
            self.spi.send(self.num, buf[i:i+4096])
