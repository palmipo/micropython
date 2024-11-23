from modbusmsg import ModbusMsg
from modbuscodec import ModbusCodec

class ModbusMsg03(ModbusMsg):
    def init(self, slaveId, bus):
        super().init(slaveId, 0x03)
        self.bus = bus

    def readHoldingRegisters(self, dataAdress, nbReg):
        self.adresse = ModbusCodec.Champ(dataAdress, 16, 16)
        self.nb = ModbusCodec.Champ(nbReg, 32, 16)
        sendBuffer = self.encode()
        recvBuffer = self.bus.transfer(sendBuffer, 3 + 2 * nbReg)
        return self.decode(recvBuffer)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(4 + len(buffer))
        bitBuffer[0:len(buffer)] = buffer

        codec = ModbusCodec()
        codec.encode(bitBuffer, self.adresse)
        codec.encode(bitBuffer, self.nb)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)
        nbReg = ModbusCodec.Champ(0x00, 16, 8)

        codec = ModbusCodec()
        codec.decode(bitBuffer, nbReg)

        res = []
        offset = 24
        for i in range(nbReg.valeur() >> 1):
            chp = ModbusCodec.Champ(0x00, offset, 16)
            res.append(codec.decode(bitBuffer, chp))
            offset += 16
        return res
