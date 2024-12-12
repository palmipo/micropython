from waveshare.waveshare_green_clock.wavesharegreenclockapps import WaveshareGreenClockApps
from waveshare.waveshare_green_clock.wavesharegreenclock import WaveshareGreenClock
import time

class WaveshareGreenClockTestApp(WaveshareGreenClockApps):
    def __init__(self, clock):
        super().__init__()
        self.clock = clock

    def cb_init(self):
        self.clock.buzzer.setDuty(99)
        time.sleep_ms(10)
        self.clock.buzzer.setDuty(0)
        for i in range(len(self.clock.buffer)):
            self.clock.buffer[i] = 0xFF
