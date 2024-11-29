import time
from waveshare.waveshare_nixie_clock.nixieclock import NixieClock
from waveshare.waveshare_nixie_clock.nixiebipapp import NixieBipApp
from waveshare.waveshare_nixie_clock.nixieconfigapp import NixieConfigApp
from waveshare.waveshare_nixie_clock.nixieledapp import NixieLedApp
from waveshare.waveshare_nixie_clock.nixiemainapp import NixieMainApp

horloge = NixieClock()
try:
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
    horloge.ds1321.setControlRegister(0, 0, 0, 0, 0)

