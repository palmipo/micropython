import machine
from interface.piabus import PiaBus

class PiaPico(PiaBus):
    def __init__(self):
        super().__init__()

    def set(self, value):
        self.pin.value(value)

    def get(self):
        return self.pin.value()

class PiaOutputPico(PiaPico):
    def __init__(self, nPin):
        super().__init__()

        self.pin = machine.Pin(nPin, machine.Pin.OUT)

class PiaInputPico(PiaPico):
    def __init__(self, nPin, pPullUp = None):
        super().__init__()

        self.pin = machine.Pin(nPin, machine.Pin.IN, pPullUp)
