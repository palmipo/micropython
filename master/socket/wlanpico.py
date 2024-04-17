import network, time, socket, select, ntptime
from lanbus import LanBus

class WLanPico(LanBus):
    def __init__(self):
        super().__init__()

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect('domoticus', '9foF2sxArWU5')
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            time.sleep(1)
        time.sleep(5)

    def disconnect(self):
        self.wlan.disconnect()

    def ifconfig(self):
        return self.wlan.ifconfig()[0]

    def ntp(self):
        ntptime.settime(timezone=1) # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
        #data_tuple = time.localtime()
        #j = "{:02}"format(data_tuple[2])
        #m = "{:02}".format(data_tuple[1])
        #a = "{:02}".format(data_tuple[0])
        #hh = "{:02}".format(data_tuple[3])
        #mm = "{:02}".format(data_tuple[4])
        #ss = "{:02}".format(data_tuple[5])
        #return j, m, a, hh, mm, ss
        return time.localtime()

