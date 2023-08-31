from devicei2c import DeviceI2C

class SAA1064(DeviceI2C):

    def __init__(self, address, bus):
        super().__init__(0x38 | (address & 0x03), bus)

    def controlRegister(self, dynamique_mode, digit_1_3, digit_2_4, test, intensity):
        cmd = bytearray(2)
        cmd[0] = 0x00 # control register
        cmd[1] = (dynamique_mode & 0x01) | ((digit_1_3 & 0x01) << 1) | ((digit_2_4 & 0x01) << 2) | ((test & 0x01) << 3) | ((intensity & 0x07) << 4)
        self.busi2c.send(self.adresse, cmd)

    def test(self, on):
        self.contrlRegister(1, 1, 1, on, 7)

    def setIntensity(self, intensity):
        self.controlRegister(1, 1, 1, 0, intensity)

    def setDigit(self, indice, valeur):
        cmd = bytearray(2)
        cmd[0] = indice & 0xff
        cmd[1] = valeur & 0xff
        self.busi2c.send(self.adresse, cmd)

    def set(self, texte):
        i = 0
        afficheur = bytearray(4)
        for i in range(len(texte)):
            afficheur[i] = self.transformation(texte[i])
            self.setDigit(i, afficheur[i])

    def transformation(self, valeur):
        switch={
            '0': return 0x3F,
            '1': return 0x06,
            '2': return 0x5B,
            '3': return 0x4F,
            '4': return 0x66,
            '5': return 0x6D,
            '6': return 0x7D,
            '7': return 0x07,
            '8': return 0x7F,
            '9': return 0x6F,
        }
