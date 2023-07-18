class ModbusRtu:
    def __init__(self, rs485):
        self.__rs485 = rs485
    
    def transfer(self, buffer):
        sendBuffer = bytearray(buffer.len + 2)
        codec.encode(sendBuffer, Champ(buffer, 0, buffer.len))
        crc = calculCrc(buffer)
        codec.encode(sendBuffer, Champ(crc, buffer.len, crc.len))
        self.__rs485.send(sendBuffer)
        
        recvBuffer = self.__rs485.recv()
        return recvBuffer
        
    def calculCrc(self, buffer):
        crc = bytearray(2)
        return crc
