from devicei2c import DeviceI2C

class PCA9685(DeviceI2C):
    
    def __init__(self, adresse, i2c):
        super().__init__(0x40 | (adresse & 0x07), i2c)