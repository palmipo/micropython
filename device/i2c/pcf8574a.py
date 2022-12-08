from devicei2c import DeviceI2C

class PCF8574A(DeviceI2C):
  def __init__(self, adresse, i2c):
    super().__init__(0x38 | (adresse & 0x07), i2c)

  def gerIODIR(self):
    return self.iodir

  def setIODIR(self, dir):
    self.iodir = dir
    self.busi2c.send(self.adresse, self.iodir)

  def setOLAT(self, value):
    self.busi2c.send(self.adresse, value|self.iodir)

  def getGPIO(self):
    return self.busi2c.recv(self.adresse, 1)[0] & self.iodir
