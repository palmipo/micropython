from modbusheader import ModbusHeader
from codec import Codec
from modbusexception import ModbusException

class ModbusMsg(ModbusHeader):
    def __init__(self, slaveId, msgId):
        super().__init__(slaveId)
        self.__msgId = Codec.Champ(msgId, 8, 8)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(1 + len(buffer))
        for i in range(len(buffer)):
            bitBuffer[i] = buffer[i]
        codec = Codec()
        codec.encode(bitBuffer, self.__msgId)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)
        msgId = Codec.Champ(0x00, 8, 8)
        codec = Codec()
        codec.decode(bitBuffer, msgId)
        if msgId.valeur() != self.__msgId.valeur():
            raise ModbusException()
