from spipico import SPIPico
from piapico import PiaPicoOutput
import time

class SPIPicoNixie(SPIPico):
    def __init__(self):
        self.csa1 = PiaPicoOutput(2)
        self.csa2 = PiaPicoOutput(3)
        self.csa3 = PiaPicoOutput(4)
        self.csa1.set(1)
        self.csa2.set(1)
        self.csa3.set(1)
        super().__init__(1, 10, 11, None)
    
    def send(self, addr, cmd):
        add = 5 - addr
#         print(add)
        try:
            self.csa1.set(add & 0x01)
            self.csa2.set((add & 0x02) >> 1)
            self.csa3.set((add & 0x04) >> 2)
#             time.sleep_ms(1)
            super().send(cmd)
#             time.sleep_ms(1)
        finally:
            self.csa1.set(1)
            self.csa2.set(1)
            self.csa3.set(1)
