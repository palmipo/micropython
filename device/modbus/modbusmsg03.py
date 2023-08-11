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
        res = [__nbReg.__valeur]
        offset = 3
        print (offset)
        print (__nbReg.__valeur)
        for i in range(__nbReg.__valeur):
            chp = Codec.Champ(0x00, offset, 16)
            codec.decode(bitBuffer, chp)
            res[i] = chp.__valeur
            offset += 2
        return res
