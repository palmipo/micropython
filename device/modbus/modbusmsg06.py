from modbusmsg import ModbusMsg
from modbuscodec import ModbusCodec

class ModbusMsg06(ModbusMsg):
    def init(self, slaveId, bus):
        super().init(slaveId, 0x06)
        self.bus = bus
        
    def presetSingleRegister(self, dataAdress, data):
        self.address = ModbusCodec.Champ(dataAdress, 16, 16)
        self.data = ModbusCodec.Champ(data, 32, 16)
        sendBuffer = self.encode()
        recvBuffer = self.bus.transfer(sendBuffer, 6)
        self.decode(recvBuffer)

    def encode(self):
        buffer = super().encode()
        bitBuffer = bytearray(4 + len(buffer))
        bitBuffer[0:len(buffer)] = buffer

        codec = ModbusCodec()
        codec.encode(bitBuffer, self.address)
        codec.encode(bitBuffer, self.data)
        return bitBuffer

    def decode(self, bitBuffer):
        super().decode(bitBuffer)
        reg_address = ModbusCodec.Champ(0x00, 16, 16)
        reg_data = ModbusCodec.Champ(0x00, 32, 16)

        codec = ModbusCodec()
        address = codec.decode(bitBuffer, reg_address)
        data = codec.decode(bitBuffer, reg_data)
        if address != self.address.valeur():
            raise ModbusException()
        if data != self.data.valeur():
            raise ModbusException()

