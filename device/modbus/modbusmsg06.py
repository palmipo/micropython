from modbusmsg import ModbusMsg
from modbuscodec import ModbusCodec

class ModbusMsg06(ModbusMsg):
    def init(self, modbus_id, bus):
        super().__init__(modbus_id, 0x06)
        self.bus = bus
        
    def presetSingleRegister(self, dataAdress, data):
        recvBuffer = self.bus.transfer(struct.pack('>BBHH', ModbusHeader.modbus_id, ModbusMsg.msg_id, dataAdress, data), 6)

        if struct.unpack('>B', recvBuffer[0]) != ModbusHeader.modbus_id:
            raise ModbusException()

        if struct.unpack('>B', recvBuffer[0]) & 0x80 != 0:
            raise ModbusException()

        if struct.unpack('>B', recvBuffer[1]) != ModbusMsg.msg_id:
            raise ModbusException()

