from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06


class R4DCB08:
    def __init__(self, modbusId, rtu):
        self.__modbusId = modbusId
        self.__rtu = rtu

    def read(self, voie):
        fc03 = ModbusMsg03(self.__modbusId, self.__rtu)
        return fc03.readHoldingRegisters(voie & 0x0F, 1)

    def readAll(self):
        fc03 = ModbusMsg03(self.__modbusId, self.__rtu)
        return fc03.readHoldingRegisters(0, 8)

