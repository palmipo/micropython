import sys

class ModbusCodec:
    class Champ:
        def __init__(self, valeur, bitDepart, nbBit):
            self.__bitDepart = bitDepart
            self.__nbBit = nbBit
            self.__valeur = valeur.to_bytes(self.nbByte(), 'big', False)

        def valeur(self):
            return int.from_bytes(self.__valeur, 'big', False)
        
        def nbByte(self):
            nb = self.__nbBit >> 3
            if (self.__nbBit % 8) > 0:
                nb = 1 + (self.__nbBit >> 3)
            return nb

        def nbBit(self):
            return self.__nbBit
        
        def bitDepart(self):
            return self.__bitDepart

    def encode(self, bitbuffer, champ):
        for i in range(champ.nbBit()):
            i_octet = i >> 3
            i_bit = i - (i_octet << 3)

            valeur = (champ.__valeur[i_octet] & (1 << i_bit)) >> i_bit

            octet = (champ.bitDepart() + i) >> 3
            bit = champ.bitDepart() + i - (octet << 3)

            bitbuffer[octet] = (bitbuffer[octet] & ~(1 << bit)) | (valeur << bit)
            
    def decode(self, bitbuffer, champ):
        champ.__valeur = bytearray(champ.nbByte())

        for i in range(champ.nbBit()):
            octet = (champ.bitDepart() + i) >> 3
            bit = champ.bitDepart() + i - (octet << 3)
            valeur = (bitbuffer[octet] & (1 << bit)) >> bit

            i_octet = i >> 3
            i_bit = i - (i_octet << 3)

            champ.__valeur[i_octet] = (champ.__valeur[i_octet] & ~(1 << i_bit)) | valeur << i_bit

        return champ.valeur()

# buf  = bytearray(8)
# chp1 = ModbusCodec.Champ(0x11, 0, 8)
# chp2 = ModbusCodec.Champ(0x03, 8, 8)
# chp3 = ModbusCodec.Champ(0x006B, 16, 16)
# chp4 = ModbusCodec.Champ(0x0003, 32, 16)
# crc  = ModbusCodec.Champ(0x7687, 48, 16)
# 
# codec = ModbusCodec()
# codec.encode(buf, chp1)
# codec.encode(buf, chp2)
# codec.encode(buf, chp3)
# codec.encode(buf, chp4)
# codec.encode(buf, crc)
# print(buf)
# 
# res = codec.decode(buf, crc)
# print(hex(res))
