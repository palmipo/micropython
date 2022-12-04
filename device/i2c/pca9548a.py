from devicei2c import DeviceI2C

class PCA9548A(DeviceI2C):

    def __init__(self, address, bus):
        super().__init__(0x70 & (address & 0x03), bus)

    def clear(self):
        cmd = bytearray(1)
        cmd[0] = 0
        self.busi2c.send(self.adresse, cmd)

    def setCanal(self, canal):
        cmd = bytearray(1)
        cmd[0] = canal & 0xff
        self.busi2c.send(self.adresse, cmd)
