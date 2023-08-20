import time
from relaybus import RelayBus
from elexol import Elexol

class ElexolRelay(RelayBus):
    def __init__(self, elexol, port):
        super().__init__()
        self.__elexol = elexol
        self.__port = port

    def read(self, voie):
        val = self.__elexol.readPort(self.__port)
        return (val & (1 << voie)) >> voie

    def open(self, voie):
        val = self.__elexol.readPort(self.__port)
        self.__elexol.writePort(self.__port, val & ~(1 << voie))

    def close(self, voie):
        val = self.__elexol.readPort(self.__port)
        self.__elexol.writePort(self.__port, val | (1 << voie))

    def toggle(self, voie):
        val = self.__elexol.readPort(self.__port) & (1 << voie)
        self.__elexol.writePort(self.__port, val ^ (1 << voie))

    def latch(self, voie):
        self.__elexol.writePort(self.__port, (1 << voie))

    def momentary(self, voie):
        val = self.__elexol.readPort(self.__port)
        self.__elexol.writePort(self.__port, val | (1 << voie))
        time.sleep(1)
        self.__elexol.writePort(self.__port, val & ~(1 << voie))

    def delay(self, voie, tempo):
        val = self.__elexol.readPort(self.__port)
        self.__elexol.writePort(self.__port, val | (1 << voie))
        time.sleep_ms(tempo)
        self.__elexol.writePort(self.__port, val & ~(1 << voie))
