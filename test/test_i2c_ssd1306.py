from oled_0_91 import OLED_0_91
from oled_1_3 import OLED_1_3
from i2cpico import I2CPico
from i2cmux import I2CMux
from pca9548a import PCA9548A
from ds1307 import DS1307
from scrollphathd import ScrollPHatHd
from lcd2004 import LCD2004
from hd44780 import HD44780
# import ntptime
# import network
import framebuf
import sys
import time

# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# addr_mac = wlan.config('mac')
# for b in addr_mac:
#     print(hex(b))
# print(wlan.config('hostname'))
# 
# wlan.connect('domoticus', '9foF2sxArWU5')
# while not wlan.isconnected() and wlan.status() >= 0:
#     time.sleep(1)
# time.sleep(10)

i2c = I2CPico(0, 4, 5) 
# circuits = i2c.scan()

switch = PCA9548A(0, i2c, 3)
switch.reset()

# ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
# data_tuple = time.localtime()
# laDate = "{:2}:{:2}:{:2}".format(str(data_tuple[2]), str(data_tuple[1]), str(data_tuple[0]))
# lHeure = "{:2}:{:2}:{:2}".format(str(data_tuple[3]), str(data_tuple[4]), str(data_tuple[5]))

mux0 = I2CMux(0, switch, i2c)
mux1 = I2CMux(1, switch, i2c)
mux6 = I2CMux(6, switch, i2c)
mux7 = I2CMux(7, switch, i2c)

lcd_io = LCD2004(0, mux6)
lcd_io.setBackLight(1)
lcd = HD44780(lcd_io)
lcd.clear()


matrix = ScrollPHatHd(mux7)
for y in range(matrix.height):
    for x in range(matrix.width):
        matrix.pixel(x, y, 0xF)
        matrix.show()
        time.sleep_ms(100)

rtc = DS1307(0, mux1)
# rtc.setDate('18/01/73')
# rtc.setDayWeek(4)
# rtc.setTime('16:30:00')

display = OLED_0_91(0, mux0)
# display = OLED_1_3(0, mux0)
display.init_display()
display.setDisplayON()
display.setEntireDisplayON()
time.sleep(1)
display.setEntireDisplayOFF()

buffer = bytearray(display.width * (display.height >> 3))
frame = framebuf.FrameBuffer(buffer, display.width, display.height, framebuf.MONO_VLSB)

while True:
    frame.fill(0)
    frame.text('Hello World !!!', 0, 0)
    frame.text(rtc.getTime(), 0, 11)
    frame.text(rtc.getDate(), 0, 22)
    display.show(buffer)

    lcd.home()
    lcd.writeText("Hello World !!!")
    lcd.setDDRAMAdrress(32)
    lcd.writeText(rtc.getTime())
    lcd.setDDRAMAdrress(20)
    lcd.writeText(rtc.getDate())
    time.sleep_ms(500)

time.sleep(5)
display.setDisplayOFF()

switch.clear()
