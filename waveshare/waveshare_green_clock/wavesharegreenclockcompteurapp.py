from waveshare.waveshare_green_clock.wavesharegreenclockapps import WaveshareGreenClockApps
from waveshare.waveshare_green_clock.wavesharegreenclock import WaveshareGreenClock
import time

class WaveshareGreenClockCompteurApp(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock
        self.cpt_gauche = 0
        self.cpt_droit = 0

    def cb_init(self):
        self.clock.tag.clear()

    def cb_up(self):
        self.cpt_gauche = (self.cpt_gauche + 1) % 100

    def cb_down(self):
        self.cpt_droit = (self.cpt_droit + 1) % 100

    def cb_center(self):
        if self.cpt_gauche != 0 or self.cpt_droit != 0:
            self.cpt_gauche = 0
            self.cpt_droit = 0
        else:
            raise NotImplementedError

    def cb_run(self):
        texte = '{:02}/{:02}'.format(self.cpt_gauche, self.cpt_droit)
        offset = 0
        for i in range(len(texte)):
            (a, w, h) = self.clock.ascii.encode(texte[i])
            for j in range(h):
                self.clock.codec.encode(self.clock.codec.Champ(self.clock.buffer, offset + 2 + (j+1) * 32, w), self.clock.codec.Champ(a, j * 8, w))
            offset += w + 1
