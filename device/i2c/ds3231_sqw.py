from device.i2c.ds3231 import DS3231
import machine

class DS3231_SQW(DS3231):
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
