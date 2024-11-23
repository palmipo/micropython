from device.i2c.ds3231 import DS3231
from master.pia.piaisrpico import PiaIsrPico

class DS3231_SQW(DS3231):
    def __init__(self, address, bus, pinSQW):
        super().__init__(address, bus)

        self.pinSQW = PiaIsrPico(pinSQW)

    def isActivated(self):
        return self.pinSQW.isActivated()
