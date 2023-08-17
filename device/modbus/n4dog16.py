from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06


class N4DOG16:
    def __init__(self, modbusId, rtu):
        self.__modbusId = modbusId
        self.__rtu = rtu

    def read(self, voie):
        fc03 = ModbusMsg03(self.__modbusId, self.__rtu)
        return fc03.readHoldingRegisters(voie & 0x1F, 1)

    def open(self, voie):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0100)

    def close(self, voie):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0200)

    def toggle(self, voie):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0300)

    def latch(self, voie):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0400)

    def momentary(self, voie):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0500)

    def delay(self, voie, tempo):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(voie & 0x1F, 0X0600 | (tempo & 0xFF))
