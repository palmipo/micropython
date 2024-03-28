import network, time, socket, select, ntptime
from lanbus import LanBus

class WLanPico(LanBus):
    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect('domoticus', '9foF2sxArWU5')
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            time.sleep(1)
        time.sleep(5)

    def disconnect(self):
        self.wlan.disconnect()

    def ntp(self):
        try:
            ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
            # data_tuple = time.localtime()
            # laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
            # lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
            return time.localtime()
        except OSError:
            pass

