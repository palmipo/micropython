import machine
from interface.piaisrbouncebus import PiaIsrBounceBus

class PiaIsrBouncePico(PiaIsrBounceBus):
    def __init__(self, nPin, tempo_ms=20, pullUp=None, trigger=machine.Pin.IRQ_FALLING):
        super().__init__(tempo_ms)

        self.pin = machine.Pin(nPin, machine.Pin.IN, pullUp)
        self.pin.irq(handler=self.isr, trigger=trigger, hard=True)

# 
# import time
# try:
#     rc = PiaIsrBouncePico(15, pullUp=machine.Pin.PULL_DOWN, trigger=machine.Pin.IRQ_FALLING)
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
