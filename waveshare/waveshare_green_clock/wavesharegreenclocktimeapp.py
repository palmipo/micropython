from waveshare.waveshare_green_clock.wavesharegreenclockapps import WaveshareGreenClockApps
from waveshare.waveshare_green_clock.wavesharegreenclock import WaveshareGreenClock
import time

class WaveshareGreenClockTimeApp(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock
        self.timezone = 0

    def cb_init(self):
        self.clock.tag.clear()
        
    def cb_up(self):
        self.timezone = (self.timezone + 1) % 24

    def cb_down(self):
        self.timezone = (self.timezone - 1) % 24

    def cb_run(self):
        data_tuple = time.localtime()
        self.heure = data_tuple[3]
        self.minute = data_tuple[4]
        self.dayOfWeek = data_tuple[6]

        self.clock.tag.clear()
        self.clock.tag.setDayWeek(self.dayOfWeek)
        lHeure = "{:02}:{:02}".format((self.heure + self.timezone) % 24, self.minute)
        offset = 0
        for i in range(len(lHeure)):
            (a, w, h) = self.clock.ascii.encode(lHeure[i])
            for j in range(h):
                self.clock.codec.encode(self.clock.codec.Champ(self.clock.buffer, offset + 2 + (j+1) * 32, w), self.clock.codec.Champ(a, j * 8, w))
            offset += w + 1
