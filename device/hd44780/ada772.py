from device.hd44780.lcd2004 import LCD2004
from device.i2c.mcp23017 import MCP23017
from device.gpio.piamcp23017 import PiaMCP23017
from master.pia.piaisrpico import PiaIsrPico
import time


class ADA772(LCD2004):

    def __init__(self, adresse, i2c, irq):
        super().__init__(adresse, i2c)

        self.BACKLIGHT = 0
        self.DB7 = 1
        self.DB6 = 2
        self.DB5 = 3
        self.DB4 = 4
        self.EN = 5
        self.RW_ = 6
        self.RS = 7

        self.gpio = MCP23017(adresse, i2c)
        self.gpio.setIOCON(0, 1, 0, 0, 0, 0, 0)
        self.gpio.setIODIR(0, 0x1f)
        self.gpio.setGPPU(0, 0x1f)
        self.gpio.setIPOL(0, 0)
        self.gpio.setGPINTEN(0, 0x1f)
        self.gpio.setINTCON(0, 0x1f)
        self.gpio.setDEFVAL(0, 0x1f)
        self.gpio.setIODIR(1, 0)

        self.irq = PiaIsrPico(irq)

        self.pia = PiaMCP23017(1, self.gpio)
        self.switchs = PiaMCP23017(0, self.gpio)

    def setBackLight(self, value):
#         print("setBackLight("+hex(value)+")")
        self.backlight = value & 0x01
        if self.backlight != 0:
            self.pia.setOutput(0)
            self.switchs.setOutput(0)
        else:
            self.pia.setOutput(1 << self.BACKLIGHT)
            self.switchs.setOutput(0xE0)

    def scrute(self):
        if self.irq.isActivated():
            sw = self.gpio.getGPIO(0)
            if sw & 1:
                print("bouton select")
            if sw & 2:
                print("bouton droit")
            if sw & 4:
                print("bouton bas")
            if sw & 8:
                print("bouton haut")
            if sw & 16:
                print("bouton gauche")
