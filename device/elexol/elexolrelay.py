import time
from interface.relaybus import RelayBus

class ElexolRelay(RelayBus):
    def __init__(self, elexol, port):
        super().init()
        self.elexol = elexol
        self.port = port

    def read(self, voie):
        val = self.elexol.readPort(self.port)
        return (val & (1 << voie)) >> voie

    def open(self, voie):
        val = self.elexol.readPort(self.port)
        self.elexol.writePort(self.port, val & ~(1 << voie))

    def close(self, voie):
        val = self.elexol.readPort(self.port)
        self.elexol.writePort(self.port, val | (1 << voie))

    def toggle(self, voie):
        val = self.elexol.readPort(self.port) & (1 << voie)
        self.elexol.writePort(self.port, val ^ (1 << voie))

    def latch(self, voie):
        self.elexol.writePort(self.port, (1 << voie))

    def momentary(self, voie):
        val = self.elexol.readPort(self.port)
        self.elexol.writePort(self.port, val | (1 << voie))
        time.sleep(1)
        self.elexol.writePort(self.port, val & ~(1 << voie))

    def delay(self, voie, tempo):
        val = self.elexol.readPort(self.port)
        self.elexol.writePort(self.port, val | (1 << voie))
        time.sleep_ms(tempo)
        self.elexol.writePort(self.port, val & ~(1 << voie))
