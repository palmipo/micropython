from devicei2c import DeviceI2C

class LSM303D(DeviceI2C):

    def __init__(self, bus):
        super().__init__(0x52, bus)

    def init(self):

    def temp_out(self):
        cmd = bytearray(1)
        cmd[0] = 0x05;
        data = self.busi2c.transferer(self.adresse, cms, 2)
        return ((data[1] << 8) | data[0])
