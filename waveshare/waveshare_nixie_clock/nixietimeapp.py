from waveshare.waveshare_nixie_clock.nixieapp import NixieApp
from waveshare.waveshare_nixie_clock.nixieclock import NixieClock
from master.net.wlanpico import WLanPico
import time, framebuf

class NixieBipApp(NixieApp):
    def __init__(self):
        super().__init__()
        self.nixie = None

    def setNixieClock(self, nixie):
        self.nixie = nixie

    def initActivated(self):
        wlan = WLanPico()
        wlan.connect()

        try:
            data_tuple = wlan.ntp()
            laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
            lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
            self.nixie.ds1321.setDate(laDate)
            self.nixie.ds1321.setDayWeek(str(data_tuple[6]))
            self.nixie.ds1321.setTime(lHeure)
        except OSError:
            pass

        for num in range(6):
            self.nixie.nixie.setLedColor(num, 0x80, 0, 0xff)
            self.nixie.dessin.fill(0x00ffffff)
            self.nixie.dessin.text("Hello World {}".format(num), 0, 0)
            self.nixie.nixie.LCDs[num].show(0, 0, self.nixie.nixie.LCDs[num].width, self.nixie.nixie.LCDs[num].height, self.nixie.buffer)
    
    def krActivated(self):
        pass

    def klActivated(self):
        pass

    def kmActivated(self):
        pass

    def rtcActivated(self):
        pass
