
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
        add = 5 - addr
#         print(add)
        try:
            self.csa1.set(add & 0x01)
            self.csa2.set((add & 0x02) >> 1)
            self.csa3.set((add & 0x04) >> 2)
#             time.sleep_ms(1)
            self.spi.send(cmd)
#             time.sleep_ms(1)
        finally:
            self.csa1.set(1)
            self.csa2.set(1)
            self.csa3.set(1)
