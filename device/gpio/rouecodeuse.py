import rp2
import time
import machine
from machine import Pin
from antirebond import AntiRebond
import micropython
micropython.alloc_emergency_exception_buf(100)

class RoueCodeuse:
    def __init__(self, pinA, pinB, pinSelect):
        self.pinA = AntiRebond(pinA, self.cb)
        self.pinB = AntiRebond(pinB, self.cb)

        self.pinS = AntiRebond(pinSelect, self.cbS, 200)

    def cbS(self):
        print("valdation")

    def cb(self, pin):
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
