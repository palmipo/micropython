from device.modbus.modbusmsg03 import ModbusMsg03
from device.modbus.eletechsup import Eletechsup

class N4DIH32(Eletechsup):
    def __init__(self, modbusId, rtu):
        super().init(modbusId, rtu)

    def read(self, voie):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(0x80 | (voie & 0x2F), 2)

    def readAll(self):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(0x00C0, 4)

if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
    bus1 = ModbusRtu(uart1)
    cpt1 = N4DIH32(0x01, bus1)
    print(cpt1.readAll())

