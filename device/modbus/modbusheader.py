from modbuscodec import ModbusCodec
from modbusexception import ModbusException

class ModbusHeader:
    def __init__(self, slaveId):
        self.__slaveId = ModbusCodec.Champ(slaveId, 0, 8)

    def encode(self):
        bitBuffer = bytearray(1)
        codec = ModbusCodec()
        codec.encode(bitBuffer, self.__slaveId)
        return bitBuffer

    def decode(self, bitBuffer):
        slaveId = ModbusCodec.Champ(0x00, 0, 8)

        codec = ModbusCodec()
        codec.decode(bitBuffer, slaveId)
        if slaveId.valeur() != self.__slaveId.valeur():
            raise ModbusException
