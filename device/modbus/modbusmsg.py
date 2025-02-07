from modbusheader import ModbusHeader
from modbuscodec import ModbusCodec
from modbusexception import ModbusException

class ModbusMsg(ModbusHeader):
    def init(self, slaveId, msgId):
        super().init(slaveId)
        self.msgId = msgId

    def encode(self):
        bitBuffer = super().encode() + struct.pack('>B', self.msgId)
        return bitBuffer

    def decode(self, bitBuffer):
        b = super().decode(bitBuffer)

        msgId = struct.unpack('>B', b[0:1])

        if msgId != self.msgId:
            raise ModbusException('msgId different de celui emis')

        if (msgId & 0x80) != 0x00:
            raise ModbusException('ModbusMsg.decode() erreur')

        return b[1:]
