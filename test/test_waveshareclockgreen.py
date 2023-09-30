import ntptime, network, framebuf, sys, time
from waveshareclockgreen import WaveshareClockGreen

width = 256
height = 7
clock = WaveshareClockGreen(width, height)
clock.column.OutputEnable()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# addr_mac = wlan.config('mac')
# for b in addr_mac:
#     print(hex(b))
# print(wlan.config('hostname'))

wlan.connect('domoticus', '9foF2sxArWU5')
while not wlan.isconnected() and wlan.status() >= 0:
    time.sleep(1)
time.sleep(10)

ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
data_tuple = time.localtime()
laDate = "{:02}:{:02}:{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
clock.rtc.setDate(laDate)
clock.rtc.setDayWeek(str(data_tuple[6]))
clock.rtc.setTime(lHeure)

buffer = bytearray((width * height) >> 3)
frame = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_HMSB) # 154 bits / 20 octets
frame.fill(0)
temp = clock.rtc.getTemperature()
frame.text("{} degres".format(str(float(temp))), 10, 0)

i=0
while True:
    clock.show(buffer, 0, 0)
    frame.scroll(-1,0)
    if i >= width:
        i=0
        frame.fill(0)
        frame.text(clock.rtc.getTime(), 0, 0)
    i+=1
        
