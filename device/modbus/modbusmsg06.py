from device.modbus.modbusmsg import ModbusMsg
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsg06(ModbusMsg):
    def __init__(self, modbus_id, bus):
        super().__init__(modbus_id, 0x06)
        self.bus = bus
        
    def presetSingleRegister(self, dataAdress, data):
        recvBuffer = self.bus.transfer(struct.pack('>BBHH', self.modbus_id, self.msg_id, dataAdress, data), 6)
#         print(recvBuffer)
        modbus_id, msg_id, addr, value = struct.unpack('>BBHH', recvBuffer)
#         print(hex(modbus_id), hex(msg_id), hex(addr), hex(value))

        if modbus_id != self.modbus_id:
            raise ModbusException()

        if msg_id & 0x80 != 0:
            raise ModbusException()

        if msg_id & 0x7F != self.msg_id:
            raise ModbusException()

        if addr != dataAdress:
            raise ModbusException()

        if value != data:
            raise ModbusException()


if __name__ == "__main__":
    from master.uart.uartpico import UartPico
    from device.modbus.modbusrtu import ModbusRtu
    import time
#     uart = UartPico(bus=1 , bdrate=9600, pinTx=4, pinRx=5)
    uart = UartPico(bus=0 , bdrate=9600, pinTx=0, pinRx=1)
    bus = ModbusRtu(uart)
    msg = ModbusMsg06(0x01, bus)
    print(msg.presetSingleRegister(0x0f, 0x01))
