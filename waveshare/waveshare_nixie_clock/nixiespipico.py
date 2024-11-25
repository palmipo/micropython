
class NixieSpiPico():
    def __init__(self, csa1, csa2, csa3, spi):
        self.csa1 = csa1
        self.csa2 = csa2
        self.csa3 = csa3
        self.csa1.set(1)
        self.csa2.set(1)
        self.csa3.set(1)
        self.spi = spi
    
    def send(self, addr, cmd):
        try:
            self.csa1.set(5 - addr & 0x01)
            self.csa2.set((5 - addr & 0x02) >> 1)
            self.csa3.set((5 - addr & 0x04) >> 2)
#             time.sleep_ms(1)
            self.spi.send(cmd)
#             time.sleep_ms(1)
        finally:
            self.csa1.set(1)
            self.csa2.set(1)
            self.csa3.set(1)
