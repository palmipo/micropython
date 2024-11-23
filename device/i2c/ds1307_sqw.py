from device.i2c.ds1307 import DS1307
from master.pia.piaisrpico import PiaIsrPico

class DS1307_SQW(DS1307):
    def __init__(self, address, bus, pinSQW):
        super().__init__(address, bus)

        self.pinSQW = PiaIsrPico(pinSQW)

    def isActivated(self):
        return self.pinSQW.isActivated()
