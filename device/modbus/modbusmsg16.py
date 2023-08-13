from modbusmsg import ModbusMsg
from codec import Codec

class ModbusMsg16(ModbusMsg):
    def __init__(self, slaveId, bus):
        super().__init__(slaveId, 0x10)
        self.__bus = bus
        
    def presetMultipleRegisters(self, dataAdress, data):
        self.__adresse = Codec.Champ(dataAdress, 16, 16)
        self.__nb_reg = Codec.Champ(len(data), 32, 16)
        self.__nb_data = Codec.Champ(len(data) << 1, 48, 8)
        self.__data = [len(data)]
        for i in range(len(data)):
            self.__data[i] = Codec.Champ(data, 56 + (i << 1), 16)
        sendBuffer = self.encode()
        recvBuffer = self.__bus.transfer(sendBuffer, 6)
        self.decode(recvBuffer)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(len(buffer) + 5 + (len(self.__data) << 1))
        for i in range(len(buffer)):
            bitBuffer[i] = buffer[i]

        codec = Codec()
        codec.encode(bitBuffer, self.__adresse)
        codec.encode(bitBuffer, self.__nb_reg)
        codec.encode(bitBuffer, self.__nb_data)
        for i in range(len(self.__data)):
            codec.encode(bitBuffer, self.__data)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)
        reg_address = Codec.Champ(0x00, 16, 16)
        reg_nbReg = Codec.Champ(0x00, 32, 16)

        codec = Codec()
        address = codec.decode(bitBuffer, reg_address)
        nbReg = codec.decode(bitBuffer, reg_nbReg)
        if address != self.__address.valeur():
            raise ModbusException()
        if nbRegs != self.__nb_reg.valeur():
            raise ModbusException()


