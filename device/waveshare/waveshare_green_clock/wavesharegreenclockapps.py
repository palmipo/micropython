

class WaveshareGreenClockApps:
    def cb_up(self):
        raise NotImplementedError

    def cb_center(self):
        raise NotImplementedError

    def cb_down(self):
        raise NotImplementedError

    def cb_rtc(self):
        raise NotImplementedError
    
    def cb_run(self, buffer):
        raise NotImplementedError
