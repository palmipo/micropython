import time, framebuf
from master.net.wlanpico import WLanPico
from waveshare.waveshare_nixie_clock.nixieclock import NixieClock
from waveshare.waveshare_nixie_clock.nixiebipapp import NixieBipApp
from waveshare.waveshare_nixie_clock.nixieconfigapp import NixieConfigApp

try:
    bipApp = NixieBipApp()
    configApp = NixieConfigApp()
    
    horloge = NixieClock([bipApp, configApp])

    bipApp.setNixieClock(horloge)
    configApp.setNixieClock(horloge)

    fin = False
    while fin == False:
        horloge.scrute()
        time.sleep_ms(500)

except KeyboardInterrupt:
    fin = True

finally:
    pass

