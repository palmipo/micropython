import rp2
import time
import machine
import micropython
micropython.alloc_emergency_exception_buf(100)

class AntiRebond:
    def __init__(self, pinA, cback, tempo=100):
        self.pinA = machine.Pin(pinA, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pinA.irq(self.cb, machine.Pin.IRQ_FALLING, hard=True)
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
