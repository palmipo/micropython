from device.modbus.modbusmsg import ModbusMsg
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsg03(ModbusMsg):
    def __init__(self, modbus_id, bus):
        super().__init__(modbus_id, 0x03)
        self.bus = bus

    def readHoldingRegisters(self, dataAdress, nbReg):
        recvBuffer = self.bus.transfer(struct.pack('>BBHH', self.modbus_id, self.msg_id, dataAdress, nbReg), 3 + 2 * nbReg)
        modbus_id, msg_id, nb_data = struct.unpack('>BBB', recvBuffer[0:3])

        if modbus_id != self.modbus_id:
            raise ModbusException()

        if msg_id & 0x80 != 0:
            raise ModbusException()

        if msg_id & 0x7F != self.msg_id:
            raise ModbusException()

        if nb_data != 2 * nbReg:
            raise ModbusException()

        data = []
        offset=3
        for i in range(nbReg):
            data.append(struct.unpack('>H', recvBuffer[offset:offset+2])[0])
            offset += 2
        return data

if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    import time
#     uart = UartPico(bus=1 , bdrate=9600, pinTx=4, pinRx=5)
    uart = UartPico(bus=0 , bdrate=9600, pinTx=0, pinRx=1)
    bus = ModbusRtu(uart)
    msg = ModbusMsg03(0x01, bus)
    print(msg.readHoldingRegisters(0x03, 0x01))
