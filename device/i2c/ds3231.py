from devicei2c import DeviceI2C

class DS3231(DeviceI2C):
    def __init__(self, adresse, i2c, pinSQW):
        super().__init__(0x68 | (address & 0x01), bus)
        self.pinSQW = Pin(pinSQW, Pin.IN, Pin.PULL_UP)
        self.pinSQW.irq(self.callback, Pin.IRQ_FALLING)

    def callback(pin):
        state = machine.disable_irq()
        self.cb()
        machine.enable_irq(state)
