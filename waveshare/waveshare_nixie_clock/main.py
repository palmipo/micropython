import time
from waveshare.waveshare_nixie_clock.nixieclock import NixieClock
from waveshare.waveshare_nixie_clock.nixiebipapp import NixieBipApp
from waveshare.waveshare_nixie_clock.nixieconfigapp import NixieConfigApp
from waveshare.waveshare_nixie_clock.nixieledapp import NixieLedApp
from waveshare.waveshare_nixie_clock.nixiemainapp import NixieMainApp
from master.net.wlanpico import WLanPico
from device.net.ntp import Ntp
from tools.configfile import ConfigFile

horloge = NixieClock()
try:
    wifi = ConfigFile("wifi.json")

    wlan = WLanPico()
    wlan.connect(wifi.config()['wifi']['ssid'], wifi.config()['wifi']['passwd'])

    ntp = Ntp()
    ntp.ntp()

    bipApp = NixieBipApp(horloge)
    configApp = NixieConfigApp(horloge)
    ledApp = NixieLedApp(horloge)

    mainApp = NixieMainApp([bipApp, configApp, ledApp])
    mainApp.init()

    fin = False
    while fin == False:
        if horloge.kr.isActivated() == True:
            mainApp.krActivated()

        if horloge.kl.isActivated() == True:
            mainApp.klActivated()

        if horloge.km.isActivated() == True:
            mainApp.kmActivated()

        if horloge.ds1321.isActivated() == True:
            mainApp.rtcActivated()

        time.sleep_ms(500)

except KeyboardInterrupt:
    pass

finally:
    fin = True
    horloge.clear()


