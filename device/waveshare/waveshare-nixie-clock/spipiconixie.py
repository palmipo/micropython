from spipico import SPIPico
from piapico import PiaPicoOutput

class SPIPicoNixie(SPIPico):
    def __init__(self):
        super().__init__(1, 10, 11, None)
        self.csa1 = PiaPicoOutput(2)
        self.csa2 = PiaPicoOutput(3)
        self.csa3 = PiaPicoOutput(4)
        self.csa1.set(1)
        self.csa2.set(1)
        self.csa3.set(1)
    
    def send(self, addr, cmd):
        add = ~addr
        try:
            self.csa1.set(add & 0x01)
            self.csa2.set((add & 0x02) >> 1)
            self.csa3.set((add & 0x04) >> 2)
            super().send(cmd)
        finally:
            self.csa1.set(1)
            self.csa2.set(1)
            self.csa3.set(1)
    
    def recv(self, addr, n_byte):
        add = ~addr
        try:
            self.csa1.set(add & 0x01)
            self.csa2.set((add & 0x02) >> 1)
            self.csa3.set((add & 0x04) >> 2)
            return super().recv(n_byte)
        finally:
            self.csa1.set(1)
            self.csa2.set(1)
            self.csa3.set(1)

