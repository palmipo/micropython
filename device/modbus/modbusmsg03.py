from modbusmsg import ModbusMsg
from codec import Codec

class ModbusMsg03(ModbusMsg):
    def __init__(self, slaveId, bus):
        super.__init(slaveId, 0x03)
        self.__bus = bus
        
    def readHoldingRegisters(self, dataAddress, nbReg):
        self.__adresse = Champ(dataAdress, 16, 16)
        self.__nb = Champ(nbReg, 24, 16)
        sendBuffer = self.encode()
        recvBuffer = self.__bus.transfer(sendBuffer)
        return self.decode(recvBuffer)

    def encode(self):
        bitBuffer = bytearray(6)
        buffer = super.encode()
        Codec.encode(bitBuffer, Champ(buffer, 0, buffer.len))
        Codec.encode(bitBuffer, self.__adresse)
        Codec.encode(bitBuffer, self.__nb)
        return bitBuffer

    def decode(self, bitBuffer):
        super.decode(bitBuffer)
        nb = Champ(1, 1)
        Codec.decode(bitBuffer, nb)
        offset = 3
        res = array('H')
        for (i=0, i<nb.__valeur; i++):
            res[i] = Codec.decode(bitBuffer, Champ(offset, 2))
            offset += 2
        return res
