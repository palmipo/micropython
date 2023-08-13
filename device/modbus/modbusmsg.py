from modbusheader import ModbusHeader
from modbuscodec import ModbusCodec
from modbusexception import ModbusException

class ModbusMsg(ModbusHeader):
    def __init__(self, slaveId, msgId):
        super().__init__(slaveId)
        self.__msgId = ModbusCodec.Champ(msgId, 8, 8)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(1 + len(buffer))
        bitBuffer[0:len(buffer)] = buffer
        codec = ModbusCodec()
        codec.encode(bitBuffer, self.__msgId)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)

        msgId = ModbusCodec.Champ(0x00, 8, 8)
        codec = ModbusCodec()
        codec.decode(bitBuffer, msgId)
        if msgId.valeur() != self.__msgId.valeur():
            raise ModbusException
