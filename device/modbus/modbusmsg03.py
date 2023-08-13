from modbusmsg import ModbusMsg
from modbuscodec import ModbusCodec

class ModbusMsg03(ModbusMsg):
    def __init__(self, slaveId, bus):
        super().__init__(slaveId, 0x03)
        self.__bus = bus
        
    def readHoldingRegisters(self, dataAdress, nbReg):
        self.__adresse = ModbusCodec.Champ(dataAdress, 16, 16)
        self.__nb = ModbusCodec.Champ(nbReg, 32, 16)
        sendBuffer = self.encode()
        recvBuffer = self.__bus.transfer(sendBuffer, 3 + 2 * nbReg)
        return self.decode(recvBuffer)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(4 + len(buffer))
        bitBuffer[0:len(buffer)] = buffer
        codec = ModbusCodec()
        codec.encode(bitBuffer, self.__adresse)
        codec.encode(bitBuffer, self.__nb)
        return bitBuffer

    def decode(self, bitBuffer):
        print(bitBuffer, len(bitBuffer))
        super().decode(bitBuffer)
        __nbReg = ModbusCodec.Champ(0x00, 16, 8)
        codec = ModbusCodec()
        codec.decode(bitBuffer, __nbReg)
        print(__nbReg.valeur())
        res = [] * (__nbReg.valeur()>>1)
        offset = 24
        for i in range(__nbReg.valeur() >> 1):
            chp = ModbusCodec.Champ(0x00, offset, 16)
            print(hex(codec.decode(bitBuffer, chp)))
            offset += 16
        return res
