from device.modbus.modbusmsg03 import ModbusMsg03
from device.modbus.eletechsup import Eletechsup

class R4DCB08(Eletechsup):
    def __init__(self, modbusId, rtu):
        super().__init__(modbusId, rtu)

    def read(self, voie):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(voie & 0x0F, 1)[0]/10

    def readAll(self):
        fc03 = ModbusMsg03(self.modbusId, self.rtu)
        return fc03.readHoldingRegisters(0, 8)


if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
    bus1 = ModbusRtu(uart1)
    cpt1 = R4DCB08(0x01, bus1)
    print(cpt1.readAll())
    print(cpt1.read(0))

