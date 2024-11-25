from waveshare.waveshare_nixie_clock.nixieapp import NixieApp
from master.net.wlanpico import WLanPico
import time

class NixieConfigWifiApp(NixieApp):
    def __init__(self, nixie):
        super().__init__()
        self.nixie = nixie

    def initActivated(self):
        for num in range(1, 6):
            self.nixie.nixie.setLedColor(num, 0x80, 0, 0xff)
            self.nixie.dessin.fill(0x00ffffff)
            self.nixie.nixie.LCDs[num].show(0, 0, self.nixie.nixie.LCDs[num].width, self.nixie.nixie.LCDs[num].height, self.nixie.buffer)

        wlan = WLanPico()
        wlan.connect()

        self.nixie.dessin.text("[wifi]", 0, 0)
        self.nixie.dessin.text("{}".format(wlan.ifconfig()), 0, 10)
        self.nixie.nixie.LCDs[1].show(0, 0, self.nixie.nixie.LCDs[1].width, self.nixie.nixie.LCDs[1].height, self.nixie.buffer)
    
    def krActivated(self):
        pass

    def klActivated(self):
        pass

    def kmActivated(self):
        pass

    def rtcActivated(self):
        pass
