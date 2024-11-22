from device.i2c.ds1307 import DS1307
import micropython
import machine

micropython.alloc_emergency_exception_buf(100)

class DS1307_SQW(DS1307):
    def __init__(self, address, bus, pinSQW):
        super().__init__(address, bus)
        self.activated = False

        self.pinSQW = machine.Pin(pinSQW, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pinSQW.irq(handler=self.callback, trigger=machine.Pin.IRQ_FALLING, hard=True)

    def callback(self, pin):
        state = machine.disable_irq()
        try:
            self.activated = True
        finally:
            machine.enable_irq(state)

    def isActivated(self):
        if self.activated == True:
            self.activated = False
            return True
        else:
            return False
