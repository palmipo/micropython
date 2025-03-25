from waveshare.waveshare_nixie_clock.nixieapp import NixieApp

class NixieLedApp(NixieApp):
    def __init__(self, nixieClock):
        super().__init__()
        self.nixieClock = nixieClock
        self.couleur = [0, 0, 0]

    def init(self):
        self.numLed = 0
        self.numCouleur = 0
        self.nixieClock.clear()
        self.show()

    def krActivated(self):
        self.couleur[self.numCouleur] = (self.couleur[self.numCouleur] + 8) % 256
        self.show()
    
    def klActivated(self):
        self.couleur[self.numCouleur] = (self.couleur[self.numCouleur] - 8) % 256
        self.show()

    def kmActivated(self):
        self.numCouleur = self.numCouleur +1
        if self.numCouleur == 3:
            self.numCouleur = 0
            self.numLed = self.numLed + 1
            if self.numLed < len(self.nixieClock.nixie.leds):
                self.show()
            else:
                self.numLed = 0
                raise NotImplementedError

    def show(self):
        self.nixieClock.nixie.setLedColor(self.numLed, self.couleur[0], self.couleur[1], self.couleur[2])

        for i in range(len(self.nixieClock.nixie.LCDs)):
            if self.numLed == i:
                # Red Green Blue (16-bit, 5+6+5) color format
                self.nixieClock.dessin.fill(((self.couleur[0] & 0x1F) << 11) | ((self.couleur[1] & 0x3F) << 5) | (self.couleur[2] & 0x1F))
                self.nixieClock.dessin.text("[LED]", 0, 0, 0xffff)
                self.nixieClock.dessin.text("R : {:03}".format(self.couleur[0]), 0, 10, 0xffff)
                self.nixieClock.dessin.text("G : {:03}".format(self.couleur[1]), 0, 20, 0xffff)
                self.nixieClock.dessin.text("B : {:03}".format(self.couleur[2]), 0, 30, 0xffff)
            else:
                self.nixieClock.dessin.fill(0)
            self.nixieClock.nixie.LCDs[i].setLcdBlackLight(99)
            self.nixieClock.nixie.LCDs[i].show(0, 0, self.nixieClock.nixie.LCDs[i].width, self.nixieClock.nixie.LCDs[i].height, self.nixieClock.buffer)

    def publisherRecev(self, topic, value):
        self.nixieClock.dessin.fill(0)
        self.nixieClock.dessin.text(topic, 0, 0, 0xffff)
        self.nixieClock.dessin.text(value, 0, 10, 0xffff)
        self.nixieClock.nixie.LCDs[5].show(0, 0, self.nixieClock.nixie.LCDs[5].width, self.nixieClock.nixie.LCDs[5].height>>1, self.nixieClock.buffer)
