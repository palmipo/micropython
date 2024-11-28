from waveshare.waveshare_nixie_clock.nixieapp import NixieApp

class NixieMainApp(NixieApp):
    def __init__(self, apps):
        super().__init__()
        self.apps = apps
        self.num = 0
        
    def init(self):
        try:
            self.apps[self.num].init()
        except NotImplementedError:
            pass

    def krActivated(self):
        try:
            self.apps[self.num].krActivated()
        except NotImplementedError:
            pass

    def klActivated(self):
        try:
            self.apps[self.num].klActivated()
        except NotImplementedError:
            pass

    def kmActivated(self):
        try:
            self.apps[self.num].kmActivated()
        except NotImplementedError:
            self.num = (self.num + 1) % len(self.apps)
            print('changement d\'appli {}'.format(self.num))
            try:
                self.apps[self.num].init()
            except NotImplementedError:
                pass

    def rtcActivated(self):
        try:
            self.apps[self.num].rtcActivated()
        except NotImplementedError:
            pass
