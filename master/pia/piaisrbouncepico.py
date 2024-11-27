import rp2, machine
from interface.piaisrbouncebus import PiaIsrBounceBus

class PiaIsrBouncePico(PiaIsrBounceBus):
    def __init__(self, nPin, tempo_ms=20, pullUp = None):
        super().__init__(tempo_ms)

        self.pin = machine.Pin(nPin, machine.Pin.IN, pullUp)
        self.pin.irq(handler=self.isr, trigger=machine.Pin.IRQ_FALLING, hard=True)

# import time
# rc = PiaIsrBouncePico(15)
# fin = False
# while fin == False:
#     print('validation {}'.format(rc.isActivated()))
#     time.sleep_ms(100)