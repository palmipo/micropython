from devicei2c import DeviceI2C

class Eeprom24C32(DeviceI2C):

    def setMemory(self, adresse, val):
        cmd = bytearray(len(val) + 1)
        cmd[0] = adresse
        for i in range(0,len(val)):
            cmd[i+1] = val & 0xff
        self.busi2c.send(self.adresse, cmd)
