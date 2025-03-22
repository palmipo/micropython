from device.modbus.modbusmsg import ModbusMsg
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsgFree(ModbusMsg):
    def __init__(self, modbus_id, msg_id, bus):
        super().__init__(modbus_id, msg_id)
        self.bus = bus

    def transfer(self, reg, msg, recvLength):
        sendBuffer = bytearray(4+len(msg))
        self.encode(sendBuffer, reg, msg)
        print(sendBuffer)
        recvBuffer = self.bus.transfer(sendBuffer, 4 + 2 * recvLength)
        return self.decode(recvBuffer)

    def encode(self, sendBuffer, reg, msg):
        super().encode(sendBuffer)
        struct.pack_into('>H', sendBuffer, 2, reg)
        sendBuffer[4:] = msg

    def decode(self, recvBuffer):
        super().decode(recvBuffer)
        reg, data = struct.unpack_from('>HH', recvBuffer, 2)
        return reg, data

if __name__ == "__main__":
    try:
        from master.uart.uartpico import UartPico
        from device.modbus.modbusrtu import ModbusRtu
        import time
        uart = UartPico(bus=0 , bdrate=9600, pinTx=0, pinRx=1)
        bus = ModbusRtu(uart)
        msg = ModbusMsgFree(1, 0x28, bus)
        print(msg.transfer(0xFE01, b'\x00\x02\x04\x00\x00\x00\x00', 0x01))
    except KeyboardInterrupt:
        print("exit")
        sys.quit()
