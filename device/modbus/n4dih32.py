from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06
from eletechsup import Eletechsup

class N4DIH32(Eletechsup):
    def init(self, modbusId, rtu):
        super().init(modbusId, rtu)

    def read(self, voie):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(0x80 | (voie & 0x2F), 2)

    def readAll(self):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(0x00C0, 4)

