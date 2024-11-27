import machine, time
from interface.piaisrbus import PiaIsrBus

class PiaIsrPico(PiaIsrBus):
    def __init__(self, nPin, pullUp = None):
        super().__init__()

        self.pin = machine.Pin(nPin, machine.Pin.IN, pullUp)
        self.pin.irq(handler=self.isr, trigger=machine.Pin.IRQ_FALLING, hard=True)

# rc = PiaIsrPico(15)
# fin = False
# while fin == False:
#     print('validation {}'.format(rc.isActivated()))
#     time.sleep_ms(50)
