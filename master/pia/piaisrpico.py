import machine, time
from interface.piaisrbus import PiaIsrBus

class PiaIsrPico(PiaIsrBus):
    def __init__(self, nPin, pPullUp=None, pTrigger=machine.Pin.IRQ_FALLING):
        super().__init__()

        self.pin = machine.Pin(nPin, machine.Pin.IN, pPullUp)
        self.pin.irq(handler=self.isr, trigger=pTrigger, hard=True)
# 
# try:
#     rc = PiaIsrPico(15, pPullUp=machine.Pin.PULL_DOWN, trigger=machine.Pin.IRQ_FALLING)
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
