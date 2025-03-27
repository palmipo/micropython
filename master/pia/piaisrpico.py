import machine, time
from interface.piaisrbus import PiaIsrBus

class PiaIsrPico(PiaIsrBus):
    def __init__(self, nPin, pullUp=None, trigger=machine.Pin.IRQ_FALLING):
        super().__init__()

        self.pin = machine.Pin(nPin, machine.Pin.IN, pullUp)
        self.pin.irq(handler=self.isr, trigger=trigger, hard=True)
      

if __name__ == "__main__":
    try:
        rc = PiaIsrPico(15, pullUp=machine.Pin.PULL_DOWN, trigger=machine.Pin.IRQ_FALLING)
        fin = False
        while fin == False:
            print('validation {}'.format(rc.isActivated()))
            time.sleep_ms(500)

    except KeyboardInterrupt:
        pass

    finally:
        fin = True
