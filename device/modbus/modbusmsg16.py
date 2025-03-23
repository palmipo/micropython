from device.modbus.modbusmsg import ModbusMsg
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsg16(ModbusMsg):
    def __init__(self, modbus_id, bus):
        super().__init__(modbus_id, 0x10)
        self.bus = bus
        
    def presetMultipleRegisters(self, dataAdress, data):
        sendBuffer = bytearray(7 + 2 * len(data))
        self.encode(sendBuffer, dataAdress, data)
        print(sendBuffer)
        recvBuffer = self.bus.transfer(sendBuffer, 6)
        print(recvBuffer)
        self.decode(recvBuffer, dataAdress, data)

    def encode(self, sendBuffer, dataAdress, data):
        super().encode(sendBuffer)
        struct.pack_into('>HHB', sendBuffer, 2, dataAdress, len(data), len(data)*2)

        offset = 7
        for i in range(len(data)):
            struct.pack_into('>H', sendBuffer, offset, data[i])
            offset += 2

    def decode(self, recvBuffer, dataAdress, data):
        super().decode(recvBuffer)

        addr, nb = struct.unpack_from('>HH', recvBuffer, 2)

        if addr != dataAdress:
            raise ModbusException()

        if nb != len(data):
            raise ModbusException()

if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    import time
#     uart = UartPico(bus=1 , bdrate=9600, pinTx=4, pinRx=5)
    uart1 = UartPico(bus=0 , bdrate=9600, pinTx=0, pinRx=1)
    bus1 = ModbusRtu(uart1)

    passwd = struct.pack('>BBHHBHH', 0x01, 0x28, 0xFE01, 0x0002, 0x04, 0x0000, 0x0000)
    recvBuffer = bus1.transfer(passwd, 6)

    time.sleep(5)
 
    try:
        msg16 = ModbusMsg16(1, bus1)
        msg16.presetMultipleRegisters(0x0f, [0x0001])
    except ModbusException:
        print('ModbusException')
