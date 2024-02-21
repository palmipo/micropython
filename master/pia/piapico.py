import rp2
from machine import Pin
from piabus import PiaBus

class PiaPico(PiaBus):
    def callback(pin):
        state = machine.disable_irq()
        try:
            self.cb()
        finally:
            machine.enable_irq(state)

    def set(self, value):
        self.pin.value(value)

    def get(self):
        return self.pin.value()

class PiaPicoOutput(PiaPico):
    def __init__(self, nPin):
        self.pin = Pin(nPin, Pin.OUT)
        super.__init__(nPin)

class PiaPicoInput(PiaPico):
    def __init__(self, nPin):
        self.pin = Pin(nPin, Pin.IN, Pin.PULL_UP)
        super.__init__()

    def __init__(self, nPin, cb):
        self.pin = Pin(nPin, Pin.IN, Pin.PULL_UP)
        self.pin.irq(self.callback, Pin.IRQ_FALLING)
        self.cb = cb
        super.__init__()
