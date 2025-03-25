from waveshare.waveshare_nixie_clock.nixieapp import NixieApp
import time

class NixieBipApp(NixieApp):
    def __init__(self, nixie):
        super().__init__()
        self.nixie = nixie
        self.valeur = [0, 99]
        self.cpt = 0

    def init(self):
        self.nixie.buzzer.setFrequency(100)
        self.nixie.clear()

    def kmActivated(self):
        self.nixie.buzzer.setPourcent(0)
        raise NotImplementedError

    def rtcActivated(self):
        self.nixie.buzzer.setPourcent(self.valeur[self.cpt])
        self.cpt = (self.cpt + 1) % len(self.valeur)

    def publisherRecev(self, topic, value):
        self.nixie.dessin.fill(0)
        self.nixie.dessin.text(topic, 0, 0, 0xffff)
        self.nixie.dessin.text(value, 0, 10, 0xffff)
        self.nixie.nixie.LCDs[5].show(0, 0, self.nixie.nixie.LCDs[5].width, self.nixie.nixie.LCDs[5].height>>1, self.nixie.buffer)
