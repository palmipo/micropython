
self.tim = machine.Timer()
self.tim .init(mode=machine.Timer.PERIODIC, freq=1000, callback=self.timer_callback)
self.timer_activayed = False

def timer_callback(self, t):
    self.timer_activayed = True
    
def isActivated(self):
    if self.timer_activayed:
        self.timer_activayed = False
        return True

    return self.timer_activayed
