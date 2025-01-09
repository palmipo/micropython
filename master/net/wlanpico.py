import network, time, json
from interface.lanbus import LanBus

class WLanPico(LanBus):
    def __init__(self):
        super().__init__()
        
        with open("/config.json", "r") as fic:
            stream = fic.read()
            self.config = json.loads(stream)

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.config['wifi']['ssid'], self.config['wifi']['passwd'])
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            time.sleep(1)
        time.sleep(5)

    def disconnect(self):
        self.wlan.disconnect()

    def ifconfig(self):
        return self.wlan.ifconfig()[0]
