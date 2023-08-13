from modbusmsg import ModbusMsg
from codec import Codec

class ModbusMsg06(ModbusMsg):
    def __init__(self, slaveId, bus):
        super().__init__(slaveId, 0x06)
        self.__bus = bus
        
    def presetSingleRegister(self, dataAdress, data):
        self.__adresse = Codec.Champ(dataAdress, 16, 16)
        self.__data = Codec.Champ(data, 32, 16)
        sendBuffer = self.encode()
        recvBuffer = self.__bus.transfer(sendBuffer, 6)
        self.decode(recvBuffer)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(4 + len(buffer))
        for i in range(len(buffer)):
            bitBuffer[i] = buffer[i]

        codec = Codec()
        codec.encode(bitBuffer, self.__adresse)
        codec.encode(bitBuffer, self.__data)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)
        reg_address = Codec.Champ(0x00, 16, 16)
        reg_data = Codec.Champ(0x00, 32, 16)

        codec = Codec()
        address = codec.decode(bitBuffer, reg_address)
        data = codec.decode(bitBuffer, reg_data)
        if address != self.__address.valeur():
            raise ModbusException()
        if data != self.__data.valeur():
            raise ModbusException()

