import network, time, ntptime, ubinascii
from master.net.wlanpico import WLanPico

wlan = WLanPico()
wlan.connect()

ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
data_tuple = time.localtime()
laDate = "{} {:02}/{:02}/{:02}".format(data_tuple[6], data_tuple[2], data_tuple[1], data_tuple[0])
lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
print(laDate)
print(lHeure)

wlan.disconnect()
