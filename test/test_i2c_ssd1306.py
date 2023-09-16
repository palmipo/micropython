from ssd1306 import SSD1306
from i2cpico import I2CPico
import framebuf
import time


i2c = I2CPico(0, 4, 5)
print(hex(i2c.scan()[0]))
 

width = 128
height = 64

buffer = bytearray(width * (height >> 3))

display = SSD1306(width, height, 0, i2c)
display.init_display()
display.setDisplayON()
display.setEntireDisplayON()
time.sleep(1)
display.setEntireDisplayOFF()

frame = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_VLSB)
frame.text('Hello World !!!', 0, 0)
display.show(buffer)

time.sleep(2)
display.setDisplayOFF()
