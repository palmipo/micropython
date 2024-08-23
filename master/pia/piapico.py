import rp2
from machine import Pin
from interface.piabus import PiaBus

class PiaPico(PiaBus):
    def __init__(self):
        super().__init__()
        
    def callback(pin):
        state = machine.disable_irq()
        try:
            if self.cb != None:
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
        super().__init__()

class PiaPicoInput(PiaPico):
    def __init__(self, nPin, cb=None):
        if cb != None:
            self.pin = Pin(nPin, Pin.IN)
        else:
            self.pin = Pin(nPin, Pin.IN, Pin.PULL_UP)
            self.pin.irq(self.callback, Pin.IRQ_FALLING)
            self.cb = cb
        super().__init__()
