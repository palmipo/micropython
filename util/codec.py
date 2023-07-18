class Champ:
    def __init__(self, bitDepart, nbBit):
        self.__init__(0, bitDepart, nbBit)
        
    def __init__(self, valeur, bitDepart, nbBit):
        self.__valeur = valeur
        self.__bitDepart = bitDepart
        self.__nbBit = nbBit
        
class Codec:
    def encode(self, bitbuffer, champ):
        for (i=0, i<champ.__nbBit; i++) :
            octet = (champ.__bitDepart + i) / 8
            bit = champ.__bitDepart - octet * 8 + i
            bitBuffer[octet] |= (bitBuffer[octet] & ~(1<<bit)) | (champ.__valeur & (1<<i))
            
    def decode(self, bitBuffer, champ):
        champ.__valeur = 0
        for (i=0, i<champ.__nbBit; i++) :
            octet = (champ.__bitDepart + i) / 8
            bit = champ.__bitDepart - octet * 8 + i
            champ.__valeur |= (champ.__valeur & ~(1<<bit)) | (bitBuffer[octet] & (1<<bit))
