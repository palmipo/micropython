import time, framebuf
from master.net.wlanpico import WLanPico
from waveshare.waveshare_nixie_clock.wavesharenixieclock import WaveshareNixieClock

try:
    horloge = WaveshareNixieClock()

    wlan = WLanPico()
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

    buffer = bytearray(horloge.nixie.width * horloge.nixie.height * 2)

    dessin = framebuf.FrameBuffer(buffer, horloge.nixie.width, horloge.nixie.height, framebuf.RGB565)

    fin = False
    while fin == False:
        for num in range(6):
            horloge.nixie.setLedColor(num, 0x80, 0, 0xff)
            dessin.fill(0x00ffffff)
            dessin.text("Hello World {}".format(num), 0, 0)
            horloge.nixie.LCDs[num].show(0, 0, horloge.nixie.width, horloge.nixie.height, buffer)
        horloge.scrute()
        time.sleep_ms(500)

except KeyboardInterrupt:
    fin = True

finally:
    wlan.disconnect()

