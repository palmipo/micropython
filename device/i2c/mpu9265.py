from devicei2c import DeviceI2C

class MPU9265(DeviceI2C):
    def __init__(self, adresse, i2c):
        super().__init__(0x68 | (adresse & 0x01), i2c)