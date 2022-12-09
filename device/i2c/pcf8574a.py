from pcf8574 import PCF8574

class PCF8574A(PCF8574):

    def __init__(self, adresse, i2c):
        super().__init__(0x38 | (adresse & 0x07), i2c)
