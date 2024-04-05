from ds1307 import DS1307
import micropython
import machine

micropython.alloc_emergency_exception_buf(100)

class DS1307_SQW(DS1307):
    def __init__(self, address, bus, pinSQW, cb):
        super().__init__(address, bus)

        if cb != None:
            self.pinSQW = machine.Pin(pinSQW, machine.Pin.IN, machine.Pin.PULL_UP)
            self.cb = cb
            self.pinSQW.irq(handler=self.callback, trigger=machine.Pin.IRQ_FALLING, hard=True)

    def callback(self, pin):
        state = machine.disable_irq()
        try:
            self.cb(pin)
        finally:
            machine.enable_irq(state)

