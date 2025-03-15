from device.modbus.modbusmsg03 import ModbusMsg03
from device.modbus.modbusmsg06 import ModbusMsg06

class Eletechsup:
    def __init__(self, modbusId, rtu):
        self.modbusId = modbusId
        self.rtu = rtu

    def getBaudRate(self):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(0x00FF, 0x0001)

    def setBaudRate(self, bdr):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(0x00FF, bdr)

    def getModbusId(self):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(0x00FE, 0x0001)

    def setModbusId(self, modbusId):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(0x00FE, bdr)

    def reset(self, ):
        fc06 = ModbusMsg06(self.modbusId, self.rtu)
        fc06.presetSingleRegister(0x00FF, 0x0005)
