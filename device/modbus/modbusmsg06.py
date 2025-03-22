from device.modbus.modbusmsg import ModbusMsg
from device.modbus.modbusexception import ModbusException
import struct

class ModbusMsg06(ModbusMsg):
    def __init__(self, modbus_id, bus):
        super().__init__(modbus_id, 0x06)
        self.bus = bus
        
    def presetSingleRegister(self, dataAdress, data):
        sendBuffer = bytearray(6)
        self.encode(sendBuffer, dataAdress, data)
        recvBuffer = self.bus.transfer(sendBuffer, 6)
        self.decode(recvBuffer, dataAdress, data)

    def encode(self, sendBuffer, dataAdress, data):
        super().encode(sendBuffer)
        struct.pack_into('>HH', sendBuffer, 2, dataAdress, data)

    def decode(self, recvBuffer, dataAdress, data):
        super().decode(recvBuffer)

        addr, value = struct.unpack_from('>HH', recvBuffer, 2)
        if addr != dataAdress:
            raise ModbusException()

        if value != data:
            raise ModbusException()

if __name__ == "__main__":
    try:
        from master.uart.uartpico import UartPico
        from device.modbus.modbusrtu import ModbusRtu
        import time
        uart = UartPico(bus=0 , bdrate=9600, pinTx=0, pinRx=1)
        bus = ModbusRtu(uart)

        try:
            msg = ModbusMsg06(0x00, bus)
            print(msg.presetSingleRegister(0x0f, 0x01))
        except ModbusException as err:
            print('ModbusException', err)
    except KeyboardInterrupt:
        print("exit")
        sys.quit()
