class WaveshareGreenClockCodec:
    class Champ:
        def __init__(self, valeur, bitDepart, nbBit):
            self.__bitDepart = bitDepart
            self.__nbBit = nbBit
            self.__valeur = valeur

        def valeur(self):
            return self.__valeur

        def nbByte(self):
            nb = self.__nbBit >> 3
            if (self.__nbBit % 8) > 0:
                nb = 1 + (self.__nbBit >> 3)
            return nb

        def nbBit(self):
            return self.__nbBit

        def bitDepart(self):
            return self.__bitDepart

    def encode(self, champDst, champSrc):
        for i in range(champSrc.nbBit()):
            
            i_octet = (champDst.bitDepart() + i) >> 3
            i_bit = champDst.bitDepart() + i - (i_octet << 3)

            octet = (champSrc.bitDepart() + i) >> 3
            bit = champSrc.bitDepart() + i - (octet << 3)

            valeur = (champSrc.__valeur[octet] & (1 << bit)) >> bit
        
            champDst.__valeur[i_octet] = (champDst.__valeur[i_octet] & ~(1 << i_bit)) | (valeur << i_bit)
