from sm5166p import SM5166P
from sm16106sc import SM16106SC
from i2cpico import I2CPico
from ds3231 import DS3231

class WaveshareClockGreen:
    def __init__(self):
        self.row = SM5166P(16, 18, 22)
        self.column = SM16106SC(11, 12, 10, 13)
        self.i2c = I2CPico(0, 6, 7)
        self.rtc = DS3231(0, i2c, 3)

        self.row.setChannel(0x07)
        data = b'\0xFF\0xFF\0xFF\0xFF'
        self.column.send(data)
        self.column.latch()
        self.column.OutputEnabled()
