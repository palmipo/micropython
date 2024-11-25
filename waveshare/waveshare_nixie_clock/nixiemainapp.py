from waveshare.waveshare_nixie_clock.nixieapp import NixieApp

class NixieMainApp(NixieApp):
    def __init__(self, apps):
        super().__init__()
        self.apps = apps
        self.num = 0

    def initActivated(self):
        pass

    def krActivated(self):
        self.apps[self.num].krActivated()

    def klActivated(self):
        self.apps[self.num].klActivated()

    def kmActivated(self):
        if self.apps[self.num].kmActivated() == None:
            self.num = (self.num + 1) % len(self.apps)
            self.apps[self.num].initActivated()

    def rtcActivated(self):
        self.apps[self.num].rtcActivated()
