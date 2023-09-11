

from ssd1306 import SSD1306

from i2cpico import I2CPico

import framebuf
import time
 

i2c = I2CPico(0, 4, 5)
print(hex(i2c.scan()[0]))
 

width = 128

height = 64

buffer = bytearray(width * height)

frame = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_VLSB)

frame.fill(1)
#frame.text('Hello World !!!', 0, 0)

display = SSD1306(width, height, 0, i2c)
#display.initDisplay()

# display.setDisplayOFF()
# display.setMemoryAddressingMode(0)
# display.setDisplayStartLine(0)
# display.setSegmentRemap()
# display.setMultiplexRatio(63)
# display.setCOMOutputScanDirection(0)
# display.setDisplayOffset(1)
# display.SetCOMPinsHardwareConfiguration(2)
# display.setDisplayClockDivideRatioOscillatorFrequency(0x0, 0x6)
# display.setPrechargePeriod(3, 0)
# display.setVCOMHDeselectLevel(0xFF)
# display.setContrastControl(0x3F)
display.setEntireDisplayOFF()
# display.setEntireDisplayON()
# display.setNormalDisplay()
# display.setChargePump(1)
# display.setDisplayON()

# display.setEntireDisplayON()
display.setNormalDisplay()
# display.setContrastControl(0x0F)
display.setDisplayON()
# display.setChargePump(1)

display.setPageAddress(0, 7)
display.setColumnAddress(0, width-1)
display.write_data(buffer[0:width-1])

# display.setColumnAddress(width, 2*width-1)
# display.write_data(buffer[width:2*width-1])
# display.write_data(buffer)

time.sleep(2)
display.setDisplayOFF()
