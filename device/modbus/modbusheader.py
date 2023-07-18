from codec import Codec

class ModbusHeader:
    def __init__(self, slaveId):
        self.__slaveId = Champ(slaveId, 0, 8)
        
    def encode(self):
        bitBuffer = bytearray(1)
        Codec.encode(bitBuffer, self.__slaveId)
        return bitBuffer
