from waveshare.waveshare_nixie_clock.nixieapp import NixieApp
from waveshare.waveshare_nixie_clock.nixieconfigwifiapp import NixieConfigWifiApp
import time

class NixieConfigApp(NixieApp):
    def __init__(self):
        super().__init__()
        self.nixie = None

    def setNixieClock(self, nixie):
        self.nixie = nixie
        self.menu = {"wifi" : NixieConfigWifiApp(nixie)}
        self.choix = "wifi"

    def initActivated(self):
        for num in range(6):
            self.nixie.nixie.setLedColor(num, 0x80, 0, 0xff)
            self.nixie.dessin.fill(0x00ffffff)
            self.nixie.nixie.LCDs[num].show(0, 0, self.nixie.nixie.LCDs[num].width, self.nixie.nixie.LCDs[num].height, self.nixie.buffer)
        
        self.nixie.dessin.text("[Config]", 0, 0)
        self.nixie.dessin.text("wifi", 0, 10)
        self.nixie.nixie.LCDs[0].show(0, 0, self.nixie.nixie.LCDs[0].width, self.nixie.nixie.LCDs[0].height, self.nixie.buffer)
    
    def krActivated(self):
#         self.choix =
        pass

    def klActivated(self):
        pass

    def kmActivated(self):
        if self.menu[self.choix].initActivated() == None:
            return 0

    def rtcActivated(self):
        pass
