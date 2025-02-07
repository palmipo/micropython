from modbusmsg import ModbusMsg
from modbuscodec import ModbusCodec

class ModbusMsg03(ModbusMsg):
    def init(self, slaveId, bus):
        super().init(slaveId, 0x03)
        self.bus = bus

    def readHoldingRegisters(self, dataAdress, nbReg):
        self.adresse = dataAdress
        self.nb = nbReg
        sendBuffer = self.encode()
        recvBuffer = self.bus.transfer(sendBuffer, 3 + 2 * nbReg)
        return self.decode(recvBuffer)

    def encode(self):
        bitBuffer = super().encode() + struct.pack('>HH', self.adresse, self.nb)
        return bitBuffer

    def decode(self, bitBuffer):
        b = super().decode(bitBuffer)
        nbReg = struct.unpack('>B', b[0:1])

        if (nbReg != self.nb):
            raise ModbusException('ModbusMsg03.decode() erreur')

        res = []
        offset=1
        for i in range(nbReg):
            res.append(struct.unpack('>H', b[offset:offset+2]))
            offset += 2
        return res
