import rp2
from machine import Pin
from interface.piabus import PiaBus

class PiaPico(PiaBus):
    def __init__(self):
        super().__init__()

    def set(self, value):
        self.pin.value(value)

    def get(self):
        return self.pin.value()

class PiaPicoOutput(PiaPico):
    def __init__(self, nPin):
        self.pin = Pin(nPin, Pin.OUT)
        super().__init__()

class PiaPicoInput(PiaPico):
    def __init__(self, nPin):
        self.pin = Pin(nPin, Pin.IN, Pin.PULL_UP)
        super().__init__()

class PiaPicoInputIsr(PiaPicoInput):
    def __init__(self, nPin):
        self.activated = False
        super().__init__(nPin)
        self.pin.irq(handler=self.callback, trigger=machine.Pin.IRQ_FALLING, hard=True)
        
    def callback(pin):
        state = machine.disable_irq()
        try:
            self.activated = True
        finally:
            machine.enable_irq(state)

    def isActivated(self):
        if self.activated == True:
            self.activated = False
            return True

        return self.activated
