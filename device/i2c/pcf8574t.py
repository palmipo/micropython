from pcf8574 import PCF8574

class PCF8574T(PCF8574):

    def __init__(self, adresse, i2c):
        super().__init__(0x3F | (adresse & 0x07), i2c)
