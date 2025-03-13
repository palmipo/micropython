from device.modbus.modbusmsg import ModbusMsg
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsg16(ModbusMsg):
    def __init__(self, modbus_id, bus):
        super().__init__(modbus_id, 0x10)
        self.bus = bus
        
    def presetMultipleRegisters(self, dataAdress, data):
        msg = struct.pack('>BBHHB', self.modbus_id, self.msg_id, dataAdress, len(data), len(data)*2)
        offset = 7
        for i in range(len(data)):
            struct.pack_into('>H', msg, offset, data[i])
            offset += 2
        recvBuffer = self.bus.transfer(msg, 6)
        modbus_id, msg_id, addr, nb = struct.unpack('>BBHH', recvBuffer)

if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    import time
#     uart = UartPico(bus=1 , bdrate=9600, pinTx=4, pinRx=5)
    uart1 = UartPico(bus=0 , bdrate=9600, pinTx=0, pinRx=1)
    bus1 = ModbusRtu(uart1)
    msg = struct.pack('>BBHHBHH', 1, 0x10, 0x07, 2, 4, 0, 0)
    recvBuffer = bus1.transfer(msg, 6)
    print(recvBuffer)
#     msg = ModbusMsg16(0x01, bus1)
#     print(msg.presetMultipleRegisters(0x0007, [0x0000, 0x0000]))
