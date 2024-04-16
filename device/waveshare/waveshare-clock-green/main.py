import ntptime, network, framebuf, sys, time, _thread
from wavesharegreenclock import WaveshareGreenClock
from wavesharegreenclockapps import WaveshareGreenClockApps
from wavesharegreenclockascii import WaveshareGreenClockAscii4x7
from wavesharegreenclockascii import WaveshareGreenClockAscii5x7
from wavesharegreenclockcodec import WaveshareGreenClockCodec
from wavesharegreenclocktag import WaveshareGreenClockTag
from wlanpico import WLanPico

class AppTime(WaveshareGreenClockApps):
    def __init__(self, buffer, *args):
        super().__init__()
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.tag = WaveshareGreenClockTag()
        self.buffer = buffer
        self.timezone = 0
        self.heure = args[3]
        self.minute = args[4]
        self.seconde = args[5]

    def cb_up(self):
        self.timezone = (self.timezone + 1) % 24

    def cb_center(self):
        pass

    def cb_down(self):
        self.timezone = (self.timezone - 1) % 24

    def cb_rtc(self):
        self.seconte = (self.seconde + 1) % 60
        if self.seconde == 0:
            self.minute = (self.minute + 1) % 60
            
            if self.minute == 0:
                self.heure = (self.heure + 1) % 24

    def cb_run(self):
        # data_tuple = time.localtime()
        # lHeure = "{:02}:{:02}".format((data_tuple[3] + self.offset) % 24, data_tuple[4])
        lHeure = "{:02}:{:02}".format((self.heure + self.timezone) % 24, self.minute)
        offset = 0
        for i in range(len(lHeure)):
            (a, w, h) = self.ascii.encode(lHeure[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(self.buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppCompteur(WaveshareGreenClockApps):
    def __init__(self, buffer):
        super().__init__()
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.cpt_gauche = 0
        self.cpt_droit = 0
        self.buffer = buffer

    def cb_up(self):
        self.cpt_gauche = (self.cpt_gauche + 1) % 100
        
    def cb_down(self):
        self.cpt_droit = (self.cpt_droit + 1) % 100

    def cb_center(self):
        pass

    def cb_rtc(self):
        pass

    def cb_run(self):
        texte = '{:02}:{:02}'.format(self.cpt_gauche, self.cpt_droit)
        offset = 0
        for i in range(len(texte)):
            (a, w, h) = self.ascii.encode(texte[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(self.buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppTemperature(WaveshareGreenClockApps):
    def __init__(self, buffer):
        super().__init__()
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.tag = WaveshareGreenClockTag()
        self.buffer = buffer

    def cb_up(self):
        pass

    def cb_center(self):
        pass

    def cb_down(self):
        pass

    def cb_rtc(self):
        pass

    def cb_run(self):
        temp = clock.rtc.getTemperature()
        texte = '{:02.1f}'.format(temp)
        offset = 0
        self.tag.uniteTemperature(buffer, b'\x01', b'\x00')
        for i in range(len(texte)):
            (a, w, h) = self.ascii.encode(texte[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(self.buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppString(WaveshareGreenClockApps):
    def __init__(self, buffer):
        super().__init__()
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.tag = WaveshareGreenClockTag()
        self.buffer = buffer

    def cb_up(self):
        pass

    def cb_center(self):
        pass

    def cb_down(self):
        pass

    def cb_rtc(self):
        pass

    def cb_run(self):
        pass

class AppMain(WaveshareGreenClockApps):
    def __init__(self, buffer, *args):
        super().__init__()
        self.cpt = 0
        self.app = [AppTime(buffer, args), AppCompteur(buffer), AppTemperature(buffer), AppString(buffer)]
        self.tag = WaveshareGreenClockTag()

    def cb_up(self):
        self.app[self.cpt].cb_up()

    def cb_center(self):
        self.tag.clear(buffer)
        self.cpt = (self.cpt + 1) % 4

    def cb_down(self):
        self.app[self.cpt].cb_down()

    def cb_rtc(self):
        self.app[self.cpt].cb_rtc()

    def cb_run(self):
        self.app[self.cpt].cb_run()


if __name__ == '__main__':
    try:
        wlan = WLanPico()
        wlan.connect()

        try:
            data_tuple = wlan.ntp()
            laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
            lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
            clock.rtc.setDate(laDate)
            clock.rtc.setDayWeek(str(data_tuple[6]))
            clock.rtc.setTime(lHeure)
        except OSError:
            pass

        buffer = bytearray(4*8)

        app = AppMain(buffer, data_tuple)

        clock = WaveshareGreenClock(app)

        fin = False
        def thread_run():
            while (True):
                clock.show(buffer)

        _thread.start_new_thread(thread_run, ());

        while (True):
            app.cb_run()
            time.sleep(1)

        wlan.disconnect()
    except KeyboardInterrupt:
        print("quit")
        quit()
