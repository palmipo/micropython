from waveshare.waveshare_nixie_clock.nixieapp import NixieApp
import time

class NixieConfigApp(NixieApp):
    def __init__(self, nixie, wlan):
        super().__init__()
        self.nixie = nixie
        self.wlan = wlan

    def init(self):
        datetime = time.localtime()
        
        # affichage WIFI
        self.nixie.dessin.fill(0)
        self.nixie.dessin.text("[wifi]", 0, 0, 0xffff)
        self.nixie.dessin.text("{}".format(self.wlan.ifconfig()), 0, 10, 0xffff)
        self.nixie.dessin.text("[date]", 0, 30, 0xffff)
        self.nixie.dessin.text("{:02}/{:02}/{:02}".format(datetime[2], datetime[1], datetime[0]), 0, 40, 0xffff)
        self.nixie.dessin.text("[time]", 0, 60, 0xffff)
        self.nixie.dessin.text("{:02}:{:02}:{:02}".format(datetime[3], datetime[4], datetime[5]), 0, 70, 0xffff)
        self.nixie.nixie.LCDs[0].show(0, 0, self.nixie.nixie.LCDs[0].width, self.nixie.nixie.LCDs[0].height, self.nixie.buffer)
        
        # affichage ALARM1
        self.nixie.dessin.fill(0)
        self.nixie.dessin.text("[alarme 1]", 0, 0, 0xffff)
        self.nixie.dessin.text("{}".format(self.nixie.ds1321.isAlarm1Activated()), 0, 10, 0xffff)
        self.nixie.nixie.LCDs[1].show(0, 0, self.nixie.nixie.LCDs[1].width, self.nixie.nixie.LCDs[1].height, self.nixie.buffer)
        
        # affichage ALARM2
        self.nixie.dessin.fill(0)
        self.nixie.dessin.text("[alarme 2]", 0, 0, 0xffff)
        self.nixie.dessin.text("{}".format(self.nixie.ds1321.isAlarm2Activated()), 0, 10, 0xffff)
        self.nixie.nixie.LCDs[2].show(0, 0, self.nixie.nixie.LCDs[2].width, self.nixie.nixie.LCDs[2].height, self.nixie.buffer)
        
        # affichage temperature DS3231
        self.nixie.dessin.fill(0)
        self.nixie.dessin.text("[Temperature]", 0, 0, 0xffff)
        self.nixie.dessin.text("{}".format(self.nixie.ds1321.getTemperature()), 0, 10, 0xffff)
        self.nixie.nixie.LCDs[3].show(0, 0, self.nixie.nixie.LCDs[3].width, self.nixie.nixie.LCDs[3].height, self.nixie.buffer)
        
        # affichage temperature BME280
        self.nixie.dessin.fill(0)
        self.nixie.dessin.text("[Temperature]", 0, 0, 0xffff)
#         self.nixie.dessin.text("{}".format(self.nixie.bmp280.compensateT()), 0, 10, 0xffff)
        self.nixie.dessin.text("[Pression]", 0, 20, 0xffff)
#         self.nixie.dessin.text("{}".format(self.nixie.bmp280.compensateP()), 0, 30, 0xffff)
        self.nixie.nixie.LCDs[4].show(0, 0, self.nixie.nixie.LCDs[4].width, self.nixie.nixie.LCDs[4].height, self.nixie.buffer)
