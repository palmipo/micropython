import ntptime
import network
import framebuf
import sys
import time
from waveshareclockgreen import WaveshareClockGreen

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

width = 256
height = 7
clock = WaveshareClockGreen(width, height)
clock.column.OutputEnable()


# ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
# data_tuple = time.localtime()
# laDate = "{:2}:{:2}:{:2}".format(str(data_tuple[2]), str(data_tuple[1]), str(data_tuple[0]))
# lHeure = "{:2}:{:2}:{:2}".format(str(data_tuple[3]), str(data_tuple[4]), str(data_tuple[5]))
# clock.rtc.setDate(laDate)
# clock.rtc.setDayWeek(str(data_tuple[6]))
# clock.rtc.setTime(lHeure)

buffer = bytearray(width * height // 8)
frame = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_HMSB) # 154 bits / 20 octets
frame.fill(0)
temp = clock.rtc.getTemperature()
frame.text("{} degres Celsius".format(str(float(temp))), 10, 0)

i=0
while True:
    clock.show(buffer, 0, 0)
    frame.scroll(-1,0)
    if i >= width:
        i=0
        frame.fill(0)
        frame.text(clock.rtc.getTime(), 0, 0)
    i+=1
        
