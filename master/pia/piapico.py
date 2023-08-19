import rp2
from machine import Pin
from piabus import PiaBus

class PiaPico(PiaBus):
    
    def __init__(self, nPin, cb):
    if cb == None:
        self.pin = Pin(nPin, Pin.OUT)
    else:
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
