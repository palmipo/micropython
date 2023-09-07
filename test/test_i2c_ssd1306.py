

from ssd1306 import SSD1306

from i2cpico import I2CPico

import framebuf

 

i2c = I2CPico(0, 4, 5)
print(hex(i2c.scan()[0]))
 

width = 128

height = 64

buffer = bytearray(width * height)

frame = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_VLSB)

#frame.fill(0)
frame.text('Hello World !!!', 0, 0)

print(buffer)

display = SSD1306(width, height, 0, i2c)
display.initDisplay()
display.show(buffer)
