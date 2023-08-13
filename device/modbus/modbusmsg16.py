from modbusmsg import ModbusMsg
from modbuscodec import ModbusCodec

class ModbusMsg16(ModbusMsg):
    def __init__(self, slaveId, bus):
        super().__init__(slaveId, 0x10)
        self.__bus = bus
        
    def presetMultipleRegisters(self, dataAdress, data):
        self.__adresse = ModbusCodec.Champ(dataAdress, 16, 16)
        self.__nb_reg = ModbusCodec.Champ(len(data), 32, 16)
        self.__nb_data = ModbusCodec.Champ(len(data) << 1, 48, 8)
        self.__data = [len(data)]
        for i in data:
            self.__data[i] = ModbusCodec.Champ(i, 56 + (i << 1), 16)
        sendBuffer = self.encode()
        recvBuffer = self.__bus.transfer(sendBuffer, 6)
        self.decode(recvBuffer)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(len(buffer) + 5 + (len(self.__data) << 1))
        bitBuffer[0:len(buffer)] = buffer

        codec = ModbusCodec()
        codec.encode(bitBuffer, self.__adresse)
        codec.encode(bitBuffer, self.__nb_reg)
        codec.encode(bitBuffer, self.__nb_data)
        for i in range(len(self.__data)):
            codec.encode(bitBuffer, self.__data)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)
        reg_address = ModbusCodec.Champ(0x00, 16, 16)
        reg_nbReg = ModbusCodec.Champ(0x00, 32, 16)

        codec = ModbusCodec()
        address = codec.decode(bitBuffer, reg_address)
        nbReg = codec.decode(bitBuffer, reg_nbReg)
        if address != self.__address.valeur():
            raise ModbusException()
        if nbRegs != self.__nb_reg.valeur():
            raise ModbusException()


