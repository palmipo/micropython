import _thread, time, machine
from waveshare.waveshare_green_clock.wavesharegreenclock import WaveshareGreenClock
from waveshare.waveshare_green_clock.wavesharegreenclockapps import WaveshareGreenClockApps
from waveshare.waveshare_green_clock.wavesharegreenclocktestapp import WaveshareGreenClockTestApp
from waveshare.waveshare_green_clock.wavesharegreenclocktimeapp import WaveshareGreenClockTimeApp
from waveshare.waveshare_green_clock.wavesharegreenclockcompteurapp import WaveshareGreenClockCompteurApp
from waveshare.waveshare_green_clock.wavesharegreenclocktemperatureapp import WaveshareGreenClockTemperatureApp

class AppMain(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.cpt = 0
        self.apps = [WaveshareGreenClockTestApp(clock), WaveshareGreenClockTimeApp(clock), WaveshareGreenClockCompteurApp(clock), WaveshareGreenClockTemperatureApp(clock)]

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
    machine.freq(240000000)

    buffer2 = bytearray(4*8)

    clock = WaveshareGreenClock()
    app = AppMain(clock)
    app.cb_init()

    fin = False
    mutex = False
    def thread_run():
        while (fin != True):
            if not mutex:
                clock.show(buffer2)

    _thread.start_new_thread(thread_run, ());

    while (fin != True):
        if clock.K0.isActivated():
            app.cb_up()

        elif clock.K1.isActivated():
            app.cb_center()

        elif clock.K2.isActivated():
            app.cb_down()

        elif clock.rtc.isActivated():
            app.cb_rtc()

        app.cb_run()
        
        mutex = True
        buffer2 = clock.buffer
        mutex = False

        time.sleep(1)

except OSError:
    pass
except KeyboardInterrupt:
    pass
finally:
    fin = True
