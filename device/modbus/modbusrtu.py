# from codec import Codec
import crcmod

class ModbusRtu:
    def __init__(self, rs485):
        self.__rs485 = rs485
    
    def transfer(self, sendBuffer, recvLen):
        print(sendBuffer, len(sendBuffer))
        crc = self.__calculCrc(sendBuffer)
        print(crc)
#         buffer = bytearray(len(sendBuffer) + 2)
#         for i in range(len(sendBuffer)):
#             buffer[i] = sendBuffer[i]
#         for i in range(len(crc)):
#             buffer[i + len(sendBuffer)] = crc[i]
        
#         recvBuffer = self.__rs485.transferer(buffer, 2 + recvLen)
#         print(recvBuffer)
#         buffer = bytearray(len(recvBuffer) - 2)
#         for i in range(len(buffer)):
#             buffer[i] = recvBuffer[i]
#         crc1 = self.calculCrc(buffer)
#         crc2 = bytearray(2)
#         for i in range(2):
#             crc2[i] = recvBuffer[i + len(buffer)]
#         return buffer
        
        def __calculCrc(self, bitBuffer):
            crc16 = crcmod.mkCrcFun(0x18005, rev=False, initCrc=0xffff)
            print(hex(crc16(bitBuffer)))
    
buffer = bytearray(b'\x11\x03\x00\x6B\x00x03')
rtu = ModbusRtu(0)
rtu.transfer(buffer, 9)