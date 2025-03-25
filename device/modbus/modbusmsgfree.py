from device.modbus.modbusmsg import ModbusMsg
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsgFree(ModbusMsg):
    def __init__(self, modbus_id, msg_id, bus):
        super().__init__(modbus_id, msg_id)
        self.bus = bus

    def transfer(self, msg, recvLength):
        sendBuffer = bytearray(2+len(msg))
        self.encode(sendBuffer, msg)
        print(sendBuffer)
        recvBuffer = self.bus.transfer(sendBuffer, 2 + recvLength)
        print(recvBuffer)
        return self.decode(recvBuffer)

    def encode(self, sendBuffer, msg):
        super().encode(sendBuffer)
        sendBuffer[2:] = msg

    def decode(self, recvBuffer):
        super().decode(recvBuffer)
        data = recvBuffer[2:]
        return data

if __name__ == "__main__":
    try:
        from master.uart.uartpico import UartPico
        from device.modbus.modbusrtu import ModbusRtu
        import time
        uart = UartPico(bus=0 , bdrate=9600, pinTx=0, pinRx=1)
        bus = ModbusRtu(uart)
        msg = ModbusMsgFree(0x01, 0x28, bus)
        print(msg.transfer(b'\xFE\x01\x00\x02\x04\x00\x00\x00\x00', 0x04))
    except KeyboardInterrupt:
        print("exit")
        sys.quit()
