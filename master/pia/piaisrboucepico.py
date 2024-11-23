import rp2, machine
from interface.piaisrbouncebus import PiaIsrBounceBus

class PiaIsrBouncePico(PiaIsrBounceBus):
    def __init__(self, nPin, tempo_ms=20):
        super().__init__(tempo_ms)

        self.pin = machine.Pin(nPin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pin.irq(handler=self.isr, trigger=machine.Pin.IRQ_FALLING, hard=True)

# rc = PiaIsrBouncePico(1)
# fin = False
# while fin == False:
#     print('validation {}'.format(rc.isActivated()))
#     time.sleep_ms(100)