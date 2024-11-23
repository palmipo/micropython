from modbusheader import ModbusHeader
from modbuscodec import ModbusCodec
from modbusexception import ModbusException

class ModbusMsg(ModbusHeader):
    def init(self, slaveId, msgId):
        super().init(slaveId)
        self.msgId = ModbusCodec.Champ(msgId, 8, 8)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(1 + len(buffer))
        bitBuffer[0:len(buffer)] = buffer
        codec = ModbusCodec()
        codec.encode(bitBuffer, self.msgId)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)

        msgId = ModbusCodec.Champ(0x00, 8, 8)
        codec = ModbusCodec()
        codec.decode(bitBuffer, msgId)
        if msgId.valeur() != self.msgId.valeur():
            raise ModbusException('msgId different de celui emis')
        if (msgId.valeur() & 0x80) != 0x00:
            raise ModbusException('msgId d\'erreur')
