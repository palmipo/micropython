from waveshare.waveshare_nixie_clock.nixieapp import NixieApp
import time

class NixieBipApp(NixieApp):
    def __init__(self, nixie):
        super().__init__()
        self.nixie = nixie
        self.valeur = [0, 99]
        self.cpt = 0
        self.activeEnergie = b'\x00'
        self.temperature = b'\x00'

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
        if topic == b'capteur/energie/0/activeEnergie':
            self.activeEnergie = value
        elif topic == b'capteur/temperature/garage':
            self.temperature = value

        self.nixie.dessin.fill(0)
        self.nixie.dessin.text("[activeEnergie]", 0, 0, 0xffff)
        self.nixie.dessin.text(self.activeEnergie, 0, 10, 0xffff)
        self.nixie.dessin.text("[temperature", 0, 20, 0xffff)
        self.nixie.dessin.text(self.temperature, 0, 30, 0xffff)
        self.nixie.nixie.LCDs[5].show(0, 0, self.nixie.nixie.LCDs[5].width, self.nixie.nixie.LCDs[5].height>>1, self.nixie.buffer)
