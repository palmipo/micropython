from waveshare.waveshare_nixie_clock.nixieapp import NixieApp
import time

class NixieBipApp(NixieApp):
    def __init__(self):
        super().__init__()
        self.nixie = None
    
    def setNixieClock(self, nixie):
        self.nixie = nixie

    def krActivated(self):
        self.nixie.buzzer.setFrequency(50)
        self.nixie.buzzer.setDuty(99)
        time.sleep_ms(10)
        self.nixie.buzzer.setDuty(0)

    def klActivated(self):
        self.nixie.buzzer.setFrequency(50)
        self.nixie.buzzer.setDuty(99)
        time.sleep_ms(10)
        self.nixie.buzzer.setDuty(0)

    def kmActivated(self):
        self.nixie.buzzer.setFrequency(50)
        self.nixie.buzzer.setDuty(99)
        time.sleep_ms(10)
        self.nixie.buzzer.setDuty(0)

    def rtcActivated(self):
        self.nixie.buzzer.setFrequency(100)
        self.nixie.buzzer.setDuty(99)
        time.sleep_ms(10)
        self.nixie.buzzer.setDuty(0)
