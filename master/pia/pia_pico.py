import rp2
from machine import Pin

class PiaPico(PIA):
    
    def __init__(self, nPin):
        self.pin = Pin(nPin)

    def cb(pin):
        state = machine.disable_irq()
        print("callback 0")
        machine.enable_irq(state)

    def setIODIR(self, value):
        self.pin.init(Pin.IN, Pin.PULL_UP)
        self.pin.irq(cb, Pin.IRQ_FALLING)
