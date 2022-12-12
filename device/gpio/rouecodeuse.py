import rp2
import time
import machine
from machine import Pin
from antirebond import AntiRebond

class RoueCodeuse:
    def __init__(self, pinA, pinB, pinSelect):
        self.pinA = Pin(pinA, Pin.IN, Pin.PULL_UP)
        self.pinA.irq(self.cb, Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.pinAValue = self.pinA.value()

        self.pinB = Pin(pinB, Pin.IN, Pin.PULL_UP)
        self.pinB.irq(self.cb, Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.pinBValue = self.pinB.value()

        self.pinS = AntiRebond(pinSelect, self.cbS, 100)

        self.newValue = 0
        self.oldValue = (self.pinAValue << 1) | self.pinBValue

        self.clic = time.ticks_cpu()

    def cbS(self):
        print("valdation")

    def cb(self, pin):
        state = machine.disable_irq()
        now = time.ticks_cpu()
        if time.ticks_diff(now, self.clic) > 100:
            self.clic = now

            self.pinAValue = self.pinA.value()
            self.pinBValue = self.pinB.value()
            self.newValue = (self.pinAValue << 1) | self.pinBValue
            if (((self.oldValue == 0) and (self.newValue == 1))
                or ((self.oldValue == 1) and (self.newValue == 3))
                or ((self.oldValue == 3) and (self.newValue == 2))
                or ((self.oldValue == 2) and (self.newValue == 0))):
                    self.sens = 1
                    print("sens +")
            else:
                if (((self.oldValue == 0) and (self.newValue == 2))
                or ((self.oldValue == 2) and (self.newValue == 3))
                or ((self.oldValue == 3) and (self.newValue == 1))
                or ((self.oldValue == 1) and (self.newValue == 0))):
                    self.sens = -1
                    print("sens -")
                else:
                    self.sens = 0
                    print("sens 0")
            
            self.oldValue = self.newValue
        machine.enable_irq(state)
