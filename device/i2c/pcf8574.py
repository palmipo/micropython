from devicei2c import DeviceI2C

class PCF8574(DeviceI2C):
    def __init__(self, adresse, i2c):
        super().__init__(adresse, i2c)
        self.iodir = 0xff

    def getIODIR(self):
        return self.iodir

    def setIODIR(self, value):
        self.iodir = value
        cmd = bytearray(1)
        cmd[0] = self.iodir
        self.busi2c.send(self.adresse, cmd)

    def setOLAT(self, value):
        cmd = bytearray(1)
        cmd[0] = value | self.iodir
        self.busi2c.send(self.adresse, cmd)

    def getGPIO(self):
        return ((self.busi2c.recv(self.adresse, 1)[0]) & self.iodir)
