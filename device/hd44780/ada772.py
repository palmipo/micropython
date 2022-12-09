from hd44780io import HD44780IO
from mcp23017 import MCP23017
from pia_mcp23017 import PIA_MCP23017
import rp2
import machine
from machine import Pin
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

    def __init__(self, adresse, i2c, isr=0, callback=None):
        super().__init__()
        self.callback = callback

        self.gpio = MCP23017(adresse, i2c)
        self.gpio.setIOCON(0, 1, 0, 0, 0, 0, 0)
        self.gpio.setIODIR(0, 0x1f)
        self.gpio.setGPPU(0, 0x1f)
        #self.gpio.setIPOL(0, 0x1f)
        self.gpio.setGPINTEN(0, 0x1f)
        self.gpio.setINTCON(0, 0x1f)
        self.gpio.setDEFVAL(0, 0x1f)
        self.gpio.setIODIR(1, 0)

        if isr != 0:
            self.pin = Pin(isr, Pin.IN, Pin.PULL_UP)
            self.pin.irq(self.scrute, Pin.IRQ_FALLING)

        self.pia = PIA_MCP23017(1, gpio)
        self.switchs = PIA_MCP23017(0, gpio)

    def setBackLight(self, value):
#         print("setBackLight("+hex(value)+")")
        self.backlight = value & 0x01
        if self.backlight != 0:
            self.pia.setOutput(0)
            self.switchs.setOutput(0)
        else:
            self.pia.setOutput(1 << BACKLIGHT)
            self.switchs.setOutput(0xE0)

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
        self.pia.setOutput((self.backlight & 0x01) | data)
        time.sleep_ms(1)
        self.pia.setOutput((self.backlight & 0x01) | data | (1 << EN))
        time.sleep_ms(2)
        self.pia.setOutput((self.backlight & 0x01) | data)
        time.sleep_ms(1)

        busy = self.isBusy()
        while busy:
            busy = self.isBusy()

    def isBusy(self):
#         print("isBusy")
        octet = self.readCmd()
        if (octet & 0x80) != 0:
            return True
        else:
            return False

    def readData(self):
#         print("readData")
        return 1

    def readCmd(self):
#         print("readCmd")
        return 1

    def write(self, data, rs, rw_, en):
        cmd = (self.backlight << BACKLIGHT) | (((data & 0x80) >> 7) << DB7) | (((data & 0x40) >> 6) << DB6) | (((data & 0x20) >> 5) << DB5) | (((data & 0x10) >> 4) << DB4) | ((rw_ & 0x01) << RW_) | ((rs & 0x01) << RS)
 
        self.pia.setOutput(cmd)
        time.sleep_ms(1)

        self.pia.setOutput(cmd | (1 << EN))
        time.sleep_ms(2)

        self.pia.setOutput(cmd)
        time.sleep_ms(1)

    def bitMode(self):
        return 0

    def nLine(self):
        return 1

    def fontMode(self):
        return 0

    def scrute(self, pin):
        print(type(pin))
        state = machine.disable_irq()
        self.gpio.getINTCAPA(0)
        sw = self.gpio.getGPIO(0)
        if sw & 1:
            print("bouton select")
            self.callback()
        if sw & 2:
            print("bouton droit")
            self.callback()
        if sw & 4:
            print("bouton bas")
            self.callback()
        if sw & 8:
            print("bouton haut")
            self.callback()
        if sw & 16:
            print("bouton gauche")
            self.callback()
        machine.enable_irq(state)
