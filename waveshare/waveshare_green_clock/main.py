import _thread, time
from waveshare.waveshare_green_clock.wavesharegreenclock import WaveshareGreenClock
from waveshare.waveshare_green_clock.wavesharegreenclockapps import WaveshareGreenClockApps

class AppTime(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock
        self.timezone = 0
        self.heure = 0 #args[3]
        self.minute = 0 #args[4]
        self.dayOfWeek = 0 #args[6]

    def cb_init(self):
        self.clock.tag.clear()
        
        data_tuple = time.localtime()
        self.heure = data_tuple[3]
        self.minute = data_tuple[4]
        self.dayOfWeek = data_tuple[6]

    def cb_up(self):
        self.timezone = (self.timezone + 1) % 24

    def cb_down(self):
        self.timezone = (self.timezone - 1) % 24

    def cb_rtc(self):
        data_tuple = time.localtime()
        self.heure = data_tuple[3]
        self.minute = data_tuple[4]
        self.dayOfWeek = data_tuple[6]

    def cb_run(self):
        self.clock.tag.clear()
        self.clock.tag.setDayWeek(self.dayOfWeek)
        lHeure = "{:02}:{:02}".format((self.heure + self.timezone) % 24, self.minute)
        offset = 0
        for i in range(len(lHeure)):
            (a, w, h) = self.clock.ascii.encode(lHeure[i])
            for j in range(h):
                self.clock.codec.encode(self.clock.codec.Champ(self.clock.buffer, offset + 2 + (j+1) * 32, w), self.clock.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppCompteur(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock
        self.cpt_gauche = 0
        self.cpt_droit = 0

    def cb_init(self):
        self.clock.tag.clear()

    def cb_up(self):
        self.cpt_gauche = (self.cpt_gauche + 1) % 100

    def cb_down(self):
        self.cpt_droit = (self.cpt_droit + 1) % 100

    def cb_center(self):
        if self.cpt_gauche != 0 or self.cpt_droit != 0:
            self.cpt_gauche = 0
            self.cpt_droit = 0
        else:
            raise NotImplementedError

    def cb_run(self):
        texte = '{:02}/{:02}'.format(self.cpt_gauche, self.cpt_droit)
        offset = 0
        for i in range(len(texte)):
            (a, w, h) = self.clock.ascii.encode(texte[i])
            for j in range(h):
                self.clock.codec.encode(self.clock.codec.Champ(self.clock.buffer, offset + 2 + (j+1) * 32, w), self.clock.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppTemperature(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock

    def cb_init(self):
        self.clock.tag.clear()

    def cb_run(self):
        temp = clock.rtc.getTemperature()
        texte = '{:02.1f}'.format(temp)
        offset = 0
        self.clock.tag.uniteTemperature(b'\x01', b'\x00')
        for i in range(len(texte)):
            (a, w, h) = self.clock.ascii.encode(texte[i])
            for j in range(h):
                self.clock.codec.encode(self.clock.codec.Champ(self.clock.buffer, offset + 2 + (j+1) * 32, w), self.clock.codec.Champ(a, j * 8, w))
            offset += w + 1

class AppTest(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock

    def cb_init(self):
        self.cpt=0
        for i in range(len(self.clock.buffer)):
            self.clock.buffer[i] = 0xFF

    def cb_rtc(self):
        self.cpt = (self.cpt + 1) % 60
        if self.cpt == 10:
            self.clock.K1.activated = True

class AppMain(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.cpt = 0
        self.apps = [AppTest(clock), AppTime(clock), AppCompteur(clock), AppTemperature(clock)]

    def cb_init(self):
        try:
            self.apps[self.cpt].cb_init()
        except NotImplementedError:
            pass

    def cb_up(self):
        try:
            self.apps[self.cpt].cb_up()
        except NotImplementedError:
            pass

    def cb_center(self):
        try:
            self.apps[self.cpt].cb_center()
        except NotImplementedError:
            self.cpt = (self.cpt + 1) % len(self.apps)
            self.apps[self.cpt].cb_init()

    def cb_down(self):
        try:
            self.apps[self.cpt].cb_down()
        except NotImplementedError:
            pass

    def cb_rtc(self):
        try:
            self.apps[self.cpt].cb_rtc()
        except NotImplementedError:
            pass

    def cb_run(self):
        try:
            self.apps[self.cpt].cb_run()
        except NotImplementedError:
            pass


try:
    buffer2 = bytearray(4*8)

    clock = WaveshareGreenClock()
    app = AppMain(clock)
    app.cb_init()

    fin = False
    def thread_run():
        while (fin != True):
            clock.show(buffer2)

    _thread.start_new_thread(thread_run, ());

    while (fin != True):
        if clock.K0.isActivated():
            app.cb_up()
            app.cb_run()
            buffer2 = clock.buffer

        elif clock.K1.isActivated():
            app.cb_center()
            app.cb_run()
            buffer2 = clock.buffer

        elif clock.K2.isActivated():
            app.cb_down()
            app.cb_run()
            buffer2 = clock.buffer

        elif clock.rtc.isActivated():
            app.cb_rtc()
            app.cb_run()
            buffer2 = clock.buffer

        time.sleep(1)

except OSError:
    pass
except KeyboardInterrupt:
    pass
finally:
    fin = True
