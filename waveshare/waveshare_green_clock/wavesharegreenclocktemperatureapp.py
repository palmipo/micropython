from waveshare.waveshare_green_clock.wavesharegreenclockapps import WaveshareGreenClockApps
from waveshare.waveshare_green_clock.wavesharegreenclock import WaveshareGreenClock
import time

class WaveshareGreenClockTemperatureApp(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock

    def cb_init(self):
        self.clock.tag.clear()

    def cb_run(self):
        temp = self.clock.rtc.getTemperature()
        texte = '{:02.1f}'.format(temp)
        offset = 0
        self.clock.tag.uniteTemperature(b'\x01', b'\x00')
        for i in range(len(texte)):
            (a, w, h) = self.clock.ascii.encode(texte[i])
            for j in range(h):
                self.clock.codec.encode(self.clock.codec.Champ(self.clock.buffer, offset + 2 + (j+1) * 32, w), self.clock.codec.Champ(a, j * 8, w))
            offset += w + 1
