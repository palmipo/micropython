from ds1307 import DS1307
from machine import Pin

class DS3231(DS1307):
    def __init__(self, address, bus, pinSQW):
        super().__init__(address, bus)
        self.pinSQW = Pin(pinSQW, Pin.IN, Pin.PULL_UP)
        self.pinSQW.irq(self.callback, Pin.IRQ_FALLING)

    def callback(pin):
        state = machine.disable_irq()
        self.cb()
        machine.enable_irq(state)

