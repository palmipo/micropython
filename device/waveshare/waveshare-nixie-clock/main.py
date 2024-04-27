import neopixel
from i2cpico import I2CPico

class WaveshareNixieClock:
    def __init__(self):
        self.wlan = WLanPico()
        self.wlan.connect()

        self.kr = PiaPicoInput(15, self.cb_kr)
        self.kl = PiaPicoInput(16, self.cb_kl)
        self.km = PiaPicoInput(17, self.cb_km)
        self.buzzer = PwmPico(14)

        self.i2c = I2CPico(0, 6, 7)
        self.bme280 = BME280(self.i2c)
        self.ds1321 = DS1321_SQW(self.i2c, 18, self.cb_rtc)

        self.led = neopixel.NeoPixel(machine.Pin.board.X22, 6)
        self.led.fill(0xff, 0xff, 0xff)
        self.led.write()
        # for i in range(6):
            # self.led[i] = (0, 0, 0)

        self.afficheurs = []
 
        try:
            data_tuple = self.wlan.ntp()
            laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
            lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
            self.ds1321.rtc.setDate(laDate)
            self.ds1321.rtc.setDayWeek(str(data_tuple[6]))
            self.ds1321.rtc.setTime(lHeure)
        except OSError:
            pass
 
    def cb_kr(self):
        pass

    def cb_kl(self):
        pass

    def cb_km(self):
        pass

    def cb_rtc(self):
        pass

if __name__ == '__main__':
    try:
        horloge = WaveshareNixieClock()
    except KeyboardInterrupt:
        print("quit")
        sys.exit()
