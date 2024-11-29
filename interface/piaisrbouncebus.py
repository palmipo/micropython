from interface.piaisrbus import PiaIsrBus
import time, machine, rp2

class PiaIsrBounceBus(PiaIsrBus):
    def __init__(self, tempo_ms=20):
        super().__init__()
        self.tempo_ms = tempo_ms
        self.t0 = time.ticks_cpu()

    def isr(self, pin):
        state = machine.disable_irq()
        try:
            now = time.ticks_cpu()
            if time.ticks_diff(now, self.t0) > self.tempo_ms:
                self.t0 = now
                self.activated = True
        finally:
            machine.enable_irq(state)
