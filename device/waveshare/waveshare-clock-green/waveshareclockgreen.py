from sm5166 import SM5166P
from sm16106 import SM16106SC
from i2cpico import I2CPico
#from ds3231 import DS3231
import framebuf

class WaveshareClockGreen:
    def __init__(self):
        self.row = SM5166P(16, 18, 22)
        self.column = SM16106SC(10, 11, 12, 13)
        self.i2c = I2CPico(1, 6, 7)
        #self.rtc = DS3231(0, i2c, 3)

buffer = bytearray(22 * 7)
frame = framebuf.FrameBuffer(buffer, 22, 7, framebuf.MONO_HLSB)
frame.text('H', 0, 0)
data = [bytearray(4), bytearray(4), bytearray(4), bytearray(4), bytearray(4), bytearray(4), bytearray(4), bytearray(4)]
clock = WaveshareClockGreen()
clock.column.OutputEnable()
j = 0
for i in range(1,8):
    data[i][0] = buffer[j]
    j+=1
    data[i][1] = buffer[j]
    j+=1
    data[i][2] = buffer[j]
    j+=1
    data[i][3] = 0x00

while True:
    for i in range(8):
        clock.column.send(data[i])
        clock.row.setChannel(i)
        clock.column.latch()
