import rp2
import time
import machine
import micropython
from master.pia.piapico import PiaPico

class AntiRebond:
    def __init__(self, pinA, cback, tempo=100):
        self.pinA = PiaPico(pinA, self.cb)
        self.callback = cback
        self.tempo = tempo

        self.clic = time.ticks_cpu()

    def cb(self, pin):
        now = time.ticks_cpu()
        if time.ticks_diff(now, self.clic) > self.tempo:
            self.callback()
            self.clic = now
