from modbusrtu import ModbusRtu
from modbusexception import ModbusException
from modbusmsg03 import ModbusMsg03
from modbusmsg06 import ModbusMsg06

class Eletechsup:
    def __init__(self, modbusId, rtu):
        self.__modbusId = modbusId
        self.__rtu = rtu

    def getBaudRate(self):
        fc03 = ModbusMsg03(self.__modbusId, self.__rtu)
        return fc03.readHoldingRegisters(0x00FF, 0x0001)

    def setBaudRate(self, bdr):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(0x00FF, bdr)

    def getModbusId(self):
        fc03 = ModbusMsg03(self.__modbusId, self.__rtu)
        return fc03.readHoldingRegisters(0x00FE, 0x0001)

    def setModbusId(self, modbusId):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(0x00FE, bdr)

    def reset(self, ):
        fc06 = ModbusMsg06(self.__modbusId, self.__rtu)
        fc06.presetSingleRegister(0x00FF, 0x0005)
