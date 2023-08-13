from modbusmsg import ModbusMsg
from codec import Codec

class ModbusMsg03(ModbusMsg):
    def __init__(self, slaveId, bus):
        super().__init__(slaveId, 0x03)
        self.__bus = bus
        
    def readHoldingRegisters(self, dataAdress, nbReg):
        self.__adresse = Codec.Champ(dataAdress, 16, 16)
        self.__nb = Codec.Champ(nbReg, 32, 16)
        sendBuffer = self.encode()
        recvBuffer = self.__bus.transfer(sendBuffer, 3 + 2 * nbReg)
        return self.decode(recvBuffer)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(4 + len(buffer))
        for i in range(len(buffer)):
            bitBuffer[i] = buffer[i]
        codec = Codec()
        codec.encode(bitBuffer, self.__adresse)
        codec.encode(bitBuffer, self.__nb)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)
        __nbReg = Codec.Champ(0x00, 16, 8)
        codec = Codec()
        codec.decode(bitBuffer, __nbReg)
        res = [__nbReg.valeur()]
        offset = 3
        for i in range(__nbReg.valeur()):
            chp = Codec.Champ(0x00, offset, 16)
            res[i] = codec.decode(bitBuffer, chp)
            offset += 2
        return res
