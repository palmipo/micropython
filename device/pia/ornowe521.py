from master.pia.piaisrpico import PiaIsrPico
import machine

class OrnoWe521:
    def __init__(self, nPin):
        self.pin = machine.Pin(nPin, machine.Pin.IN)
        self.pin.irq(handler=self.isr, trigger=machine.Pin.IRQ_FALLING, hard=True)
        self.cpt = 0

    def isr(self, pin):
        state = machine.disable_irq()
        try:
            self.cpt += 1
        finally:
            machine.enable_irq(state)

    def compteur(self):
        return self.cpt


if __name__ == "__main__":
    import time
    try:
        rc = OrnoWe521(15)
        fin = False
        while fin == False:
            print('compteur {}'.format(rc.compteur()))
            time.sleep(60)

    except KeyboardInterrupt:
        fin = True
