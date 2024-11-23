import sys

class ModbusCodec:
    class Champ:
        def init(self, valeur, bitDepart, nbBit):
            self.bitDepart = bitDepart
            self.nbBit = nbBit
            self.valeur = valeur.to_bytes(self.nbByte(), 'big', False)

        def valeur(self):
            return int.from_bytes(self.valeur, 'big', False)

        def nbByte(self):
            nb = self.nbBit >> 3
            if (self.nbBit % 8) > 0:
                nb = 1 + (self.nbBit >> 3)
            return nb

        def nbBit(self):
            return self.nbBit

        def bitDepart(self):
            return self.bitDepart

    def encode(self, bitbuffer, champ):
        for i in range(champ.nbBit()):
            i_octet = i >> 3
            i_bit = i - (i_octet << 3)

            valeur = (champ.valeur[i_octet] & (1 << i_bit)) >> i_bit

            octet = (champ.bitDepart() + i) >> 3
            bit = champ.bitDepart() + i - (octet << 3)

            bitbuffer[octet] = (bitbuffer[octet] & ~(1 << bit)) | (valeur << bit)

    def decode(self, bitbuffer, champ):
        champ.valeur = bytearray(champ.nbByte())

        for i in range(champ.nbBit()):
            octet = (champ.bitDepart() + i) >> 3
            bit = champ.bitDepart() + i - (octet << 3)
            valeur = (bitbuffer[octet] & (1 << bit)) >> bit

            i_octet = i >> 3
            i_bit = i - (i_octet << 3)

            champ.valeur[i_octet] = (champ.valeur[i_octet] & ~(1 << i_bit)) | (valeur << i_bit)

        return champ.valeur()
