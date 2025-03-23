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

    def rtcActivated(self):
        self.nixie.buzzer.setPourcent(self.valeur[self.cpt])
        self.cpt = (self.cpt + 1) % len(self.valeur)