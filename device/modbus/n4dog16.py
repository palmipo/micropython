from device.modbus.modbusmsg03 import ModbusMsg03
from device.modbus.modbusmsg06 import ModbusMsg06
from device.modbus.eletechsup import Eletechsup

class N4DOG16(Eletechsup):
    def __init__(self, modbusId, rtu):
        super().__init__(modbusId, rtu)

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


if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
    bus1 = ModbusRtu(uart1)
    cpt1 = N4DOG16(0x01, bus1)
    cpt1.momentary(0)

