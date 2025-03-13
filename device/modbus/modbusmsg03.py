from modbusmsg import ModbusMsg
from modbuscodec import ModbusCodec

class ModbusMsg03(ModbusMsg):
    def __init__(self, modbus_id, bus):
        super().init(modbus_id, 0x03)
        self.bus = bus

    def readHoldingRegisters(self, dataAdress, nbReg):
        recvBuffer = self.bus.transfer(struct.pack('>BBHH', super().modbus_id, super().msg_id, dataAdress, nbReg), 3 + 2 * nbReg)
        modbus_id, msg_id, nb_data = struct.unpack('>BBB', recvBuffer[0:3])

        if struct.unpack('>B', recvBuffer[0]) != ModbusHeader.modbus_id:
            raise ModbusException()

        if struct.unpack('>B', recvBuffer[0]) & 0x80 != 0:
            raise ModbusException()

        if struct.unpack('>B', recvBuffer[1]) != ModbusMsg.msg_id:
            raise ModbusException()

        data = []
        offset=3
        for i in range(nbReg):
            data.append(struct.unpack('>H', recvBuffer[offset:offset+2]))
            offset += 2
        return data
