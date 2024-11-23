from device.pwm.l298n import L298N
from device.spi.st7735 import TFT
from device.spi.sysfont import sysfont
from master.pwmpico import PwmPico
import time, machine

bl = PwmPico(45)
bl.setFrequency(100000)
bl.setDuty(50)

tft = TFT(spi=machine.SPI(1, baudrate=8000000, sck=machine.Pin(10), mosi=machine.Pin(11), polarity=0, phase=0), aDC=18, aReset=21, aCS=9)
tft.init_7735(tft.GREENTAB80x160)
tft.fill(TFT.BLACK)
tft.text((0, 0), 'Hello World',TFT.WHITE, sysfont, 1)

# buz1 = L298N(34, 35, 36, 1)
# buz2 = L298N(37, 38, 39, 1)
# buz1.forward(32767)
# buz2.forward(32767)
# time.sleep(10)
# 
# buz1.reverse(32767)
# buz2.reverse(32767)
# 
# time.sleep(10)
# 
# buz1.off()
# buz2.off()
