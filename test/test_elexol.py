from master.elexol.elexol import Elexol
from device.elexol.elexolrelay import ElexolRelay

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

