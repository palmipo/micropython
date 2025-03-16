from device.modbus.modbusmsg import ModbusMsg
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsg03(ModbusMsg):
    def __init__(self, modbus_id, bus):
        super().__init__(modbus_id, 0x03)
        self.bus = bus

    def readHoldingRegisters(self, dataAdress, nbReg):
        sendBuffer = bytearray(6)
        self.encode(sendBuffer, dataAdress, nbReg)
        recvBuffer = self.bus.transfer(sendBuffer, 3 + 2 * nbReg)
        return self.decode(recvBuffer, nbReg)

    def encode(self, sendBuffer, dataAdress, nbReg):
        super().encode(sendBuffer)
        struct.pack_into('>HH', sendBuffer, 2, dataAdress, nbReg)

    def decode(self, recvBuffer, nbReg):
        super().decode(recvBuffer)
        nb_data = struct.unpack_from('>B', recvBuffer, 2)[0]
        if nb_data != 2 * nbReg:
            raise ModbusException()

        data = []
        offset=3
        for i in range(nbReg):
            data.append(struct.unpack_from('>H', recvBuffer, offset)[0])
            offset += 2
        return data

if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    import time
    uart = UartPico(bus=0 , bdrate=9600, pinTx=0, pinRx=1)
    bus = ModbusRtu(uart)
    msg = ModbusMsg03(0, bus)
    print(msg.readHoldingRegisters(0x02, 0x01))
