import time, framebuf
from master.net.wlanpico import WLanPico
from waveshare.waveshare_nixie_clock.nixieclock import NixieClock
from waveshare.waveshare_nixie_clock.nixiebipapp import NixieBipApp

wlan = WLanPico()
try:
    bipApp = NixieBipApp()
    horloge = NixieClock([bipApp])
    bipApp.setNixieClock(horloge)

    wlan.connect()

    try:
        data_tuple = wlan.ntp()
        laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
        lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
        horloge.ds1321.setDate(laDate)
        horloge.ds1321.setDayWeek(str(data_tuple[6]))
        horloge.ds1321.setTime(lHeure)
    except OSError:
        pass

    buffer = bytearray(horloge.nixie.LCDs[0].width * horloge.nixie.LCDs[0].height * 2)

    dessin = framebuf.FrameBuffer(buffer, horloge.nixie.LCDs[0].width, horloge.nixie.LCDs[0].height, framebuf.RGB565)

    for num in range(6):
        horloge.nixie.setLedColor(num, 0x80, 0, 0xff)
        dessin.fill(0x00ffffff)
        dessin.text("Hello World {}".format(num), 0, 0)
        horloge.nixie.LCDs[num].show(0, 0, horloge.nixie.LCDs[num].width, horloge.nixie.LCDs[num].height, buffer)

    fin = False
    while fin == False:
        horloge.scrute()
        time.sleep_ms(500)

except KeyboardInterrupt:
    fin = True

finally:
#     wlan.disconnect()
    pass

