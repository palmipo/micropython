import ntptime, network, framebuf, sys, time, _thread
from wavesharegreenclock import WaveshareGreenClock
from wavesharegreenclockapps import WaveshareGreenClockApps
from wavesharegreenclockascii import WaveshareGreenClockAscii4x7
from wavesharegreenclockascii import WaveshareGreenClockAscii5x7
from wavesharegreenclockcodec import WaveshareGreenClockCodec
from wavesharegreenclocktag import WaveshareGreenClockTag
from wlanpico import WLanPico

class AppTime(WaveshareGreenClockApps):
    def __init__(self, buffer):
        super().__init__()
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.tag = WaveshareGreenClockTag(buffer)
        self.buffer = buffer
        self.timezone = 0
        self.heure = 0 #args[3]
        self.minute = 0 #args[4]
        self.seconde = 0 #args[5]
        self.dayOfWeek = 0 #args[6]

    def cb_init(self):
        self.tag.clear()
        
        data_tuple = time.localtime()
        self.heure = data_tuple[3]
        self.minute = data_tuple[4]
        self.seconde = data_tuple[5]
        self.dayOfWeek = data_tuple[6]

    def cb_up(self):
        self.timezone = (self.timezone + 1) % 24
        return 0

    def cb_center(self):
        pass

    def cb_down(self):
        self.timezone = (self.timezone - 1) % 24
        return 0

    def cb_rtc(self):
        self.seconde = (self.seconde + 1) % 60
        if self.seconde == 0:
            self.minute = (self.minute + 1) % 60
            if self.minute == 0:
                self.heure = (self.heure + 1) % 24
                if self.heure == 0:
                    self.dayOfWeek = (self.dayOfWeek + 1) % 7

    def cb_run(self):
        self.tag.setDayWeek(self.dayOfWeek)
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
        self.tag = WaveshareGreenClockTag(buffer)
        self.cpt_gauche = 0
        self.cpt_droit = 0
        self.buffer = buffer

    def cb_init(self):
        self.tag.clear()

    def cb_up(self):
        self.cpt_gauche = (self.cpt_gauche + 1) % 100
        return 0

    def cb_down(self):
        self.cpt_droit = (self.cpt_droit + 1) % 100
        return 0

    def cb_center(self):
        if self.cpt_gauche != 0 or self.cpt_droit != 0:
            self.cpt_gauche = 0
            self.cpt_droit = 0
            return 0

    def cb_rtc(self):
        pass

    def cb_run(self):
        texte = '{:02}/{:02}'.format(self.cpt_gauche, self.cpt_droit)
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
        self.tag = WaveshareGreenClockTag(buffer)
        self.buffer = buffer

    def cb_init(self):
        self.tag.clear()

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
        self.tag.uniteTemperature(b'\x01', b'\x00')
        for i in range(len(texte)):
            (a, w, h) = self.ascii.encode(texte[i])
            for j in range(h):
                self.codec.encode(self.codec.Champ(self.buffer, offset + 2 + (j+1) * 32, w), self.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppTest(WaveshareGreenClockApps):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def cb_init(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 0xFF

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
    def __init__(self, buffer):
        super().__init__()
        self.cpt = 0
        self.apps = [AppTest(buffer), AppTime(buffer), AppCompteur(buffer), AppTemperature(buffer)]
        self.tag = WaveshareGreenClockTag(buffer)
        self.apps[self.cpt].cb_init()

    def cb_init(self):
        pass

    def cb_up(self):
        self.apps[self.cpt].cb_up()

    def cb_center(self):
        if self.apps[self.cpt].cb_center() == None:
            self.cpt = (self.cpt + 1) % len(self.apps)
            self.apps[self.cpt].cb_init()

    def cb_down(self):
        self.apps[self.cpt].cb_down()

    def cb_rtc(self):
        for app in self.apps:
            app.cb_rtc()

    def cb_run(self):
        self.apps[self.cpt].cb_run()


if __name__ == '__main__':
    try:
    
        buffer = bytearray(4*8)
        buffer2 = bytearray(4*8)

        app = AppMain(buffer)

        clock = WaveshareGreenClock()

        try:
            wlan = WLanPico()
            wlan.connect()
            data_tuple = wlan.ntp()

            laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
            lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])

            clock.rtc.setDate(laDate)
            clock.rtc.setDayWeek(str(data_tuple[6]))
            clock.rtc.setTime(lHeure)
        except OSError:
            pass
        finally:
            wlan.disconnect()

        fin = False
        def thread_run():
            while (fin != True):
                clock.show(buffer2)

        _thread.start_new_thread(thread_run, ());

        while (fin != True):
            if clock.is_k0_beat():
                app.cb_up()
            elif clock.is_k1_beat():
                app.cb_center()
            elif clock.is_k2_beat():
                app.cb_down()
            elif clock.is_rtc_beat():
                app.cb_rtc()

            app.cb_run()
            buffer2 = buffer
            time.sleep_ms(500)

    except OSError:
        fin = True
        print("quit")
        sys.exit()
    except KeyboardInterrupt:
        fin = True
        print("quit")
        sys.exit()
