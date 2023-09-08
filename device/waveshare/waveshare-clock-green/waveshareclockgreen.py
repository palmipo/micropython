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

buffer = bytearray(24 * 8)
#frame = framebuf.FrameBuffer(buffer, 24, 8, framebuf.MONO_HLSB)
#frame.text('H', 0, 1)
#frame.fill(2)

print(buffer)

clock = WaveshareClockGreen()
clock.column.OutputEnable()

while True:
    for i in range(8):
        clock.column.send(buffer[i*24:i*24+24])
        clock.row.setChannel(i)
        clock.column.latch()
