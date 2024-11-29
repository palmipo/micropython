import machine
from interface.piaisrbouncebus import PiaIsrBounceBus

class PiaIsrBouncePico(PiaIsrBounceBus):
    def __init__(self, nPin, tempo_ms=20, pPullUp=None, pTrigger=machine.Pin.IRQ_FALLING):
        super().__init__(tempo_ms)

        self.pin = machine.Pin(nPin, machine.Pin.IN, pPullUp)
        self.pin.irq(handler=self.isr, trigger=pTrigger, hard=True)

# 
# import time
# try:
#     rc = PiaIsrBouncePico(15, pPullUp=machine.Pin.PULL_DOWN, trigger=machine.Pin.IRQ_FALLING)
#     fin = False
#     while fin == False:
#         print('validation {}'.format(rc.isActivated()))
#         time.sleep_ms(500)
# 
# except KeyboardInterrupt:
#     pass
# 
# finally:
#     fin = True
