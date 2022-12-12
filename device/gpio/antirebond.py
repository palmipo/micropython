import rp2
import time
import machine
from machine import Pin

class AntiRebond:
    def __init__(self, pinA, cback, tempo=100):
        self.pinA = Pin(pinA, Pin.IN, Pin.PULL_UP)
        self.pinA.irq(self.cb, Pin.IRQ_FALLING)
        self.callback = cback
        self.tempo = tempo

        self.clic = time.ticks_cpu()

    def cb(self, pin):
        state = machine.disable_irq()
        now = time.ticks_cpu()
        if time.ticks_diff(now, self.clic) > self.tempo:
            self.callback()
            self.clic = now
        machine.enable_irq(state)
