from codec import Codec

class ModbusHeader:
    def __init__(self, slaveId):
        self.__slaveId = Codec.Champ(slaveId, 0, 8)

    def encode(self):
        bitBuffer = bytearray(1)
        codec = Codec()
        codec.encode(bitBuffer, self.__slaveId)
        return bitBuffer

    def decode(self, bitBuffer):
        codec = Codec()
        codec.decode(bitBuffer, self.__slaveId)
