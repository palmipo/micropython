from modbusheader import ModbusHeader
from codec import Codec

class ModbusMsg(ModbusHeader):
    def __init__(self, slaveId, msgId):
        super.__init__(slaveId)
        self.__msgId = Champ(msgId, 8, 8)
        
    def encode(self):
        bitBuffer = bytearray(2)
        buffer = super.encode()
        Codec.encode(bitBuffer, Champ(buffer, 0, buffer.len))
        Codec.encode(bitBuffer, self.__msgId)
        return bitBuffer
