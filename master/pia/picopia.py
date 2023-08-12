import rp2
from machine import Pin
from buspia import BusPia

class PicoPia(BusPia):
    
    def __init__(self, nPin, cb):
        self.pin = Pin(nPin, Pin.IN, Pin.PULL_UP)
        self.pin.irq(self.callback, Pin.IRQ_FALLING)
        self.cb = cb

    def callback(pin):
        state = machine.disable_irq()
        self.cb()
        machine.enable_irq(state)

    def setOutput(self, value):
        self.pin.value(value)

    def getInput(self):
        return self.pin.value()
