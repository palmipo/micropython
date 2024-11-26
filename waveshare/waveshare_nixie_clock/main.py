import time
from waveshare.waveshare_nixie_clock.nixieclock import NixieClock
from waveshare.waveshare_nixie_clock.nixiebipapp import NixieBipApp
from waveshare.waveshare_nixie_clock.nixieconfigapp import NixieConfigApp
from waveshare.waveshare_nixie_clock.nixiemainapp import NixieMainApp

try:

    horloge = NixieClock()

    bipApp = NixieBipApp(horloge)
    configApp = NixieConfigApp(horloge)

    mainApp = NixieMainApp([bipApp, configApp])
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
    fin = True

finally:
    pass

