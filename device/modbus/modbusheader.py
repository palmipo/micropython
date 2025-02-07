from modbusexception import ModbusException
import struct

class ModbusHeader:
    def init(self, slaveId):
        self.slaveId = slaveId

    def encode(self):
        bitBuffer = struct.pack('>B', self.slaveId)
        return bitBuffer

    def decode(self, bitBuffer):
        slaveId = struct.unpack('>B', bitBuffer[0:1])

        if slaveId != self.slaveId:
            raise ModbusException('ModbusHeader.decode() erreur')

        return bitBuffer[1:]
