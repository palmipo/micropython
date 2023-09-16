from oled_0_91 import OLED_0_91
from oled_1_3 import OLED_1_3
from i2cpico import I2CPico
import framebuf
import time


i2c = I2CPico(0, 4, 5) 

display = OLED_0_91(0, i2c)
# display = OLED_1_3(0, i2c)
display.init_display()
display.setDisplayON()
display.setEntireDisplayON()
time.sleep(1)
display.setEntireDisplayOFF()

buffer = bytearray(display.width * (display.height >> 3))
frame = framebuf.FrameBuffer(buffer, display.width, display.height, framebuf.MONO_VLSB)
frame.text('Hello World !!!', 0, 0)
display.show(buffer)

time.sleep(5)
display.setDisplayOFF()
