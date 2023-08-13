from modbusexception import ModbusException

class ModbusRtu:
    def __init__(self, rs485):
        self.__rs485 = rs485
    
    def transfer(self, sendBuffer, recvLen):
        print(sendBuffer, len(sendBuffer))
        crc = self.__calcul_crc(sendBuffer)
        print(crc)

        buffer = bytearray(len(sendBuffer) + 2)
        buffer[0:len(sendBuffer)] = sendBuffer
        buffer[len(sendBuffer):] = crc
        
        recvBuffer = self.__rs485.transfer(buffer, recvLen + 2)
        print(recvBuffer, len(recvBuffer), recvLen)

        buffer = recvBuffer[0:recvLen]
        crc1 = recvBuffer[recvLen:]
        crc2 = self.__calcul_crc(buffer)
        print(crc1, crc2)
        if crc1 != crc2:
            raise ModbusException
        return buffer
        
    def __calcul_crc(self, bitBuffer):
        return bytearray(b'\x49\xAD')

# buffer = bytearray(b'\x11\x03\x00\x6B\x00x03')
# rtu = ModbusRtu(0)
# rtu.transfer(buffer, 9)