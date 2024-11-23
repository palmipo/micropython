from modbuscodec import ModbusCodec
from modbusexception import ModbusException

class ModbusHeader:
    def init(self, slaveId):
        self.slaveId = ModbusCodec.Champ(slaveId, 0, 8)

    def encode(self):
        bitBuffer = bytearray(1)
        codec = ModbusCodec()
        codec.encode(bitBuffer, self.slaveId)
        return bitBuffer

    def decode(self, bitBuffer):
        slaveId = ModbusCodec.Champ(0x00, 0, 8)

        codec = ModbusCodec()
        codec.decode(bitBuffer, slaveId)
        if slaveId.valeur() != self.slaveId.valeur():
            raise ModbusException
