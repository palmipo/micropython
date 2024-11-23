from modbusmsg import ModbusMsg
from modbuscodec import ModbusCodec

class ModbusMsg16(ModbusMsg):
    def init(self, slaveId, bus):
        super().init(slaveId, 0x10)
        self.bus = bus
        
    def presetMultipleRegisters(self, dataAdress, data):
        self.adresse = ModbusCodec.Champ(dataAdress, 16, 16)
        self.nb_reg = ModbusCodec.Champ(len(data), 32, 16)
        self.nb_data = ModbusCodec.Champ(len(data) << 1, 48, 8)
        self.data = [len(data)]
        for i in data:
            self.data[i] = ModbusCodec.Champ(i, 56 + (i << 1), 16)
        sendBuffer = self.encode()
        recvBuffer = self.bus.transfer(sendBuffer, 6)
        self.decode(recvBuffer)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(len(buffer) + 5 + (len(self.data) << 1))
        bitBuffer[0:len(buffer)] = buffer

        codec = ModbusCodec()
        codec.encode(bitBuffer, self.adresse)
        codec.encode(bitBuffer, self.nb_reg)
        codec.encode(bitBuffer, self.nb_data)
        for i in range(len(self.data)):
            codec.encode(bitBuffer, self.data)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)
        reg_address = ModbusCodec.Champ(0x00, 16, 16)
        reg_nbReg = ModbusCodec.Champ(0x00, 32, 16)

        codec = ModbusCodec()
        address = codec.decode(bitBuffer, reg_address)
        nbReg = codec.decode(bitBuffer, reg_nbReg)
        if address != self.address.valeur():
            raise ModbusException()
        if nbRegs != self.nb_reg.valeur():
            raise ModbusException()


