from interface.piabus import PiaBus
import machine

class PiaIsrBus(PiaBus):
    def __init__(self):
        super().__init__()
        self.activated = False

    def isr(self, pin):
        state = machine.disable_irq()
        try:
            self.activated = True
        finally:
            machine.enable_irq(state)

    def isActivated(self):
        if self.activated == True:
            self.activated = False

        return self.activated
