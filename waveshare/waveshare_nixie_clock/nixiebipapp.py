from waveshare.waveshare_nixie_clock.nixieapp import NixieApp
import time

class NixieBipApp(NixieApp):
    def __init__(self, nixie):
        super().__init__()
        self.nixie = nixie

    def rtcActivated(self):
        self.nixie.buzzer.setFrequency(100)
        self.nixie.buzzer.setDuty(99)
        time.sleep_ms(10)
        self.nixie.buzzer.setDuty(0)
