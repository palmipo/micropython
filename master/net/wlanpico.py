import network, time, json
from interface.lanbus import LanBus

class WLanPico(LanBus):
    def __init__(self):
        super().__init__()
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self, ssid, passwd):
        self.wlan.connect(ssid, passwd)
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            time.sleep(1)
        time.sleep(1)

    def disconnect(self):
        self.wlan.disconnect()

    def ifconfig(self):
        return self.wlan.ifconfig()[0]


if __name__ == "__main__":
    from tools.configfile import ConfigFile
    from device.net.ntp import Ntp
    
    wlan = WLanPico()
    try:
        wifi = ConfigFile("wifi.json")
        wlan.connect(wifi.config()['wifi']['ssid'], wifi.config()['wifi']['passwd'])
        print(wlan.ifconfig())
    except OSError:
        print('erreur OSError')

    finally:
        print('deconnexion')
        wlan.disconnect()


