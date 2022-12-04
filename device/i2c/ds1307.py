from devicei2c import DeviceI2C

class DS1307(DeviceI2C):

    jour = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche")

    def setDayWeek(self, day):
        cmd = bytearray(2)
        cmd[0] = 0x03
        cmd[1] = int(day) & 0x07
        self.busi2c.send(self.adresse, cmd)

    def getDayWeek(self):
        cmd = bytearray(1)
        cmd[0] = 0x03
        data = self.busi2c.transferer(self.adresse, cmd, 1)
        return self.jour[int(data[0]) & 0x07]

    #18/01/73
    def setDate(self, date):
        cmd = bytearray(4)
        cmd[0] = 0x04
        cmd[1] = ((int(date[0]) & 0x03) << 4) | (int(date[1]) & 0x0F)
        cmd[2] = ((int(date[3]) & 0x01) << 4) | (int(date[4]) & 0x0F)
        cmd[3] = ((int(date[6]) & 0x0F) << 4) | (int(date[7]) & 0x0F)
        self.busi2c.send(self.adresse, cmd)

    def getDate(self):
        cmd = bytearray(1)
        cmd[0] = 0x04
        data = self.busi2c.transferer(self.adresse, cmd, 3)
        return str((int(data[0]) & 0x30) >> 4) + str(int(data[0]) & 0x0F) + "/" + str((int(data[1]) & 0x10) >> 4) + str(int(data[1]) & 0x0F) + "/" + str((int(data[2]) & 0xF0) >> 4) + str(int(data[2]) & 0x0F)

    #18:25:59
    def setTime(self, hour):
        cmd = bytearray(4)
        cmd[0] = 0x00
        cmd[1] = ((int(hour[6]) & 0x07) << 4) | (int(hour[7]) & 0x0F)
        cmd[2] = ((int(hour[3]) & 0x07) << 4) | (int(hour[4]) & 0x0F)
        cmd[3] = ((int(hour[0]) & 0x03) << 4) | (int(hour[1]) & 0x0F)
        self.busi2c.send(self.adresse, cmd)

    def getTime(self):
        cmd = bytearray(1)
        cmd[0] = 0x00
        data = self.busi2c.transferer(self.adresse, cmd, 3)
        return str((int(data[2]) & 0x30) >> 4) + str(int(data[2]) & 0x0F) + ":" + str((int(data[1]) & 0x70) >> 4) + str(int(data[1]) & 0x0F) + ":" + str((int(data[0]) & 0x70) >> 4) + str(int(data[0]) & 0x0F)

    def setOut(self, etat):
        cmd = bytearray(2)
        cmd[0] = 0x07
        cmd[1] = (etat & 0x01) << 7
        self.busi2c.send(self.adresse, cmd)

    def setSquareWave(self, freq):
        cmd = bytearray(2)
        cmd[0] = 0x07
        cmd[1] = (freq & 0x03) | (1 << 4)
        self.busi2c.send(self.adresse, cmd)

    def setMemory(self, adresse, valeur):
        cmd = bytearray(2)
        cmd[0] = 0x08 + adresse
        cmd[1] = valeur & 0xff
        self.busi2c.send(self.adresse, cmd)

    def getMemory(self, adresse):
        if adresse < 56:
            cmd = bytearray(1)
            cmd[0] = 0x08 + adresse
            data = self.busi2c.transferer(self.adresse, cmd, 1)
            return int(data[0])
