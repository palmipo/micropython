import ntptime, network, framebuf, sys, time, _thread
from wavesharegreenclock import WaveshareGreenClock
from wavesharegreenclockapps import WaveshareGreenClockApps
from wavesharegreenclockascii import WaveshareGreenClockAscii4x7
from wavesharegreenclockascii import WaveshareGreenClockAscii5x7
from wavesharegreenclockcodec import WaveshareGreenClockCodec
from wavesharegreenclocktag import WaveshareGreenClockTag
from wlanpico import WLanPico

class AppTime(WaveshareGreenClockApps):
    def __init__(self):
        super().__init__()
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.tag = WaveshareGreenClockTag()

    def cb_up(self):
        pass

    def cb_center(self):
        pass

    def cb_down(self):
        pass

    def cb_rtc(self):
        pass
    
    def run(self, buffer):
        data_tuple = time.localtime()
        lHeure = "{:02}:{:02}".format(data_tuple[3], data_tuple[4])
        
        offset = 0
        for i in range(len(lHeure)):
            (a, w, h) = self.ascii.encode(lHeure[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppCompteur(WaveshareGreenClockApps):
    def __init__(self):
        super().__init__()
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.cpt_gauche = 0
        self.cpt_droit = 0

    def cb_up(self):
        self.cpt_gauche += 1

    def cb_down(self):
        self.cpt_droit += 1

    def cb_center(self):
        pass

    def cb_rtc(self):
        pass

    def run(self, buffer):
        texte = '{:02}:{:02}'.format(self.cpt_gauche, self.cpt_droit)
        offset = 0
        for i in range(len(texte)):
            (a, w, h) = self.ascii.encode(texte[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppTemperature(WaveshareGreenClockApps):
    def __init__(self):
        super().__init__()
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.tag = WaveshareGreenClockTag()

    def cb_up(self):
        pass

    def cb_center(self):
        pass

    def cb_down(self):
        pass

    def cb_rtc(self):
        pass

    def run(self, buffer):
        temp = clock.rtc.getTemperature()
        texte = '{:02.1f}'.format(temp)
        offset = 0
        self.tag.uniteTemperature(buffer, b'\x01', b'\x00')
        for i in range(len(texte)):
            (a, w, h) = self.ascii.encode(texte[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1


class AppMain(WaveshareGreenClockApps):
    def __init__(self):
        super().__init__()
        self.cpt = 1
        self.app = AppTime()

    def cb_up(self):
        self.app.cb_up()

    def cb_center(self):
        if self.cpt == 0:
            self.app = AppTime()
            self.cpt = 1
            
        elif self.cpt == 1:
            self.app = AppCompteur()
            self.cpt = 2
            
        elif self.cpt == 2:
            self.app = AppTemperature()
            self.cpt = 0

    def cb_down(self):
        self.app.cb_down()

    def cb_rtc(self):
        self.app.cb_rtc()

    def run(self, buffer):
        self.app.run(buffer)

wlan = WLanPico()
wlan.connect()

app = AppMain()

ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
data_tuple = time.localtime()
laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])

clock = WaveshareGreenClock(app)
clock.rtc.setDate(laDate)
clock.rtc.setDayWeek(str(data_tuple[6]))
clock.rtc.setTime(lHeure)

fin = False
buffer = bytearray(4*8)
mutex = _thread.allocate_lock()

def thread_run():
    while (True):
        mutex.acquire(-1, -1)
        mutex.locked()
        clock.show(buffer)
        mutex.release()

_thread.start_new_thread(thread_run, ());

while (True):
    mutex.acquire(-1, -1)
    mutex.locked()
    app.run(buffer)
    mutex.release()
    time.sleep(10)

wlan.disconnect()
