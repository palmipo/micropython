import network, time

class WLanPico(WLanBus):
    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect('domoticus', '9foF2sxArWU5')
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            time.sleep(1)
        time.sleep(5)

    def disconnect(self):
        wlan.disconnect()
