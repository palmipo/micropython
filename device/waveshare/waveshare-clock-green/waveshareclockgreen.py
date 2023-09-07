from sm5166 import SM5166P
from sm16106 import SM16106SC
from i2cpico import I2CPico
#from ds3231 import DS3231

class WaveshareClockGreen:
    def __init__(self):
        self.row = SM5166P(16, 18, 22)
        self.column = SM16106SC(10, 11, 12, 13)
        self.i2c = I2CPico(1, 6, 7)
        #self.rtc = DS3231(0, i2c, 3)

data = bytearray(4)
clock = WaveshareClockGreen()
clock.column.OutputEnable()
data[0] = 0xFF
data[1] = 0xFF
data[2] = 0xFF
#data[3] = 0x00

while True:
    clock.column.send(data)
    for i in range(7):
        clock.row.setChannel(i)
        clock.column.latch()
