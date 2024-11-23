from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06
from eletechsup import Eletechsup

class N4DOG16(Eletechsup):
    def init(self, modbusId, rtu):
        super().init(modbusId, rtu)

    def read(self, voie):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(voie & 0x1F, 1)

    def open(self, voie):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0100)

    def close(self, voie):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0200)

    def toggle(self, voie):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0300)

    def latch(self, voie):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0400)

    def momentary(self, voie):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0500)

    def delay(self, voie, tempo):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0600 | (tempo & 0xFF))
