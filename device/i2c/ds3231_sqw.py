from device.i2c.ds3231 import DS3231
import micropython
import machine

micropython.alloc_emergency_exception_buf(100)

class DS3231_SQW(DS3231):
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

