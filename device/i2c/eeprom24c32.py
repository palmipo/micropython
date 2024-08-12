from device.i2c.devicei2c import DeviceI2C

class Eeprom24C32(DeviceI2C):

    def __init__(self, bus):
        super().__init__(0x50, bus)

    def write(self, adresse, val):
        cmd = bytearray(len(val) + 2)
        cmd[0] = (adresse & 0xFF00) >> 8
        cmd[1] = adresse & 0x00FF
        for i in range(0,len(val)):
            cmd[i+2] = val & 0xff
        self.busi2c.send(self.adresse, cmd)

    def read(self, adresse):
        cmd = bytearray(2)
        cmd[0] = (adresse & 0xFF00) >> 8
        cmd[1] = adresse & 0x00FF
        return self.busi2c.send(self.adresse, cmd)
