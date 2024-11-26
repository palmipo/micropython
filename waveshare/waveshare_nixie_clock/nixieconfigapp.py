from waveshare.waveshare_nixie_clock.nixieapp import NixieApp

class NixieConfigApp(NixieApp):
    def __init__(self, nixie):
        super().__init__()
        self.nixie = nixie

    def init(self):
        for num in range(len(self.nixie.nixie.LCDs)):
            self.nixie.nixie.setLedColor(num, 0x80, 0, 0xff)
            self.nixie.dessin.fill(0x00ffffff)
            self.nixie.nixie.LCDs[num].show(0, 0, self.nixie.nixie.LCDs[num].width, self.nixie.nixie.LCDs[num].height, self.nixie.buffer)
        
        # affichage WIFI
        self.nixie.dessin.text("[wifi]", 0, 0)
        self.nixie.dessin.text("{}".format(self.nixie.wlan.ifconfig()), 0, 10)
        self.nixie.nixie.LCDs[0].show(0, 0, self.nixie.nixie.LCDs[0].width, self.nixie.nixie.LCDs[0].height, self.nixie.buffer)
