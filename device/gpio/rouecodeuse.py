import rp2
import machine
from machine import Pin

class RoueCodeuse:
    def __init__(self, pinA, pinB):
        self.pinA = Pin(pinA, Pin.IN, Pin.PULL_UP)
        self.pinA.irq(self.cbA, Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.pinAValue = self.pinA.value()

        self.pinB = Pin(pinB, Pin.IN, Pin.PULL_UP)
        self.pinB.irq(self.cbB, Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.pinBValue = self.pinB.value()

        self.newValue = (self.pinAValue << 1) | self.pinBValue
        self.oldValue = self.newValue

    def cbA(self, pin):
        self.pinAValue = self.pinA.value()
        self.oldValue = self.newValue
        self.newValue = (self.pinAValue << 1) | self.pinBValue

    def cbB(self, pin):
        self.pinBValue = self.pinB.value()
        self.oldValue = self.newValue
        self.newValue = (self.pinAValue << 1) | self.pinBValue
