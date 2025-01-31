import time
from interface.relaybus import RelayBus

class ElexolRelay(RelayBus):
    def __init__(self, elexol, port):
        super().__init__()
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

if __name__ == "__main__":
    from master.elexol.elexol import Elexol
    from tools.configfile import ConfigFile
    cfg = ConfigFile('master/net/wifi.json')
    from master.net.wlanpico import WLanPico
    wlan = WLanPico()
    try:
        wlan.connect(cfg.config()['wifi']['ssid'], cfg.config()['wifi']['passwd'])
        print(wlan.ifconfig())

        io = Elexol()
        io.connect("192.168.1.120")
        print(io.identifyIO24Units())
        io.setDirectionPort(0, 0xff)
        io.setDirectionPort(1, 0)
        io.setDirectionPort(2, 0)

        print(hex(io.readPort(0)))

        relay = ElexolRelay(io, 2)
        relay.momentary(2)
        io.disconnect()
    finally:
        wlan.disconnect()

