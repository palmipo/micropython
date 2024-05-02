import time
from machine import Pin
from neopixel import NeoPixel
from wlanpico import WLanPico
from i2cpico import I2CPico
from ds3231_sqw import DS3231_SQW

class WaveshareNixieClock:
    def __init__(self):
        self.wlan = WLanPico()
        self.wlan.connect()

#         self.kr = PiaPicoInput(15, self.cb_kr)
#         self.kl = PiaPicoInput(16, self.cb_kl)
#         self.km = PiaPicoInput(17, self.cb_km)
#         self.buzzer = PwmPico(14)

        self.i2c = I2CPico(1, 6, 7)
#         self.bme280 = BME280(self.i2c)
        self.ds1321 = DS3231_SQW(0, self.i2c, 18, self.cb_rtc)
        self.ds1321.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)

        self.led = NeoPixel(Pin(22, Pin.OUT), 6)
        for i in range(6):
            self.led[i] = (0x0f, 0x00, 0x00)
        self.led.write()

#         self.afficheurs = []
 
        try:
            data_tuple = self.wlan.ntp()
            laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
            lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
            self.ds1321.setDate(laDate)
            self.ds1321.setDayWeek(str(data_tuple[6]))
            self.ds1321.setTime(lHeure)
        except OSError:
            pass
 
    def cb_kr(self):
        pass

    def cb_kl(self):
        pass

    def cb_km(self):
        pass

    def cb_rtc(self, pin):
        print("rtc")

if __name__ == '__main__':
    try:
        horloge = WaveshareNixieClock()
        time.sleep(60)
    except KeyboardInterrupt:
        print("quit")
        sys.exit()
