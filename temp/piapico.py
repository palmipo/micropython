import rp2, machine
from piabus import PiaBus

class PiaPico(PiaBus):
    def __init__(self):
        super().__init__()
        
    def callback(self, pin):
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
        self.pin = machine.Pin(nPin, machine.Pin.OUT)
        super().__init__()

class PiaPicoInput(PiaPico):
    def __init__(self, nPin, cb=None):
        self.pin = machine.Pin(nPin, machine.Pin.IN)#, machine.Pin.PULL_UP)

        if cb != None:
            self.pin.irq(handler=self.callback, trigger=machine.Pin.IRQ_FALLING, hard=True)
            self.cb = cb

        super().__init__()

            
if __name__=='__main__':
    import time
    import sys    
    try:
        buz = PiaPicoOutput(14)
        buz.set(1)
        time.sleep_ms(10)
        buz.set(0)
        time.sleep_ms(10)
    except KeyboardInterrupt:
        sys.exit()
