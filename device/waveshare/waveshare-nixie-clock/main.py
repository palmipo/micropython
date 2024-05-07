import time
from machine import Pin
from neopixel import NeoPixel
from wlanpico import WLanPico
from i2cpico import I2CPico
from ds3231 import DS3231
# from ds3231_sqw import DS3231_SQW
import sys
from lcdnixie import Lcd_1inch14
from piapico import PiaPicoOutput, PiaPicoInput
from pwmpico import PwmPico
from spipiconixie import SPIPicoNixie

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
        self.ds1321 = DS3231(0, self.i2c)
#         self.ds1321 = DS3231_SQW(0, self.i2c, 18, self.cb_rtc)
#         self.ds1321.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)

        dc=PiaPicoOutput(8)
        rst=PiaPicoOutput(12)
        spi=SPIPicoNixie()
        bl=PwmPico(13)
        led=NeoPixel(Pin(22, Pin.OUT), 6)
        self.afficheurs = [Lcd_1inch14(0, dc, rst, spi, bl, led)]
 
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
        print("cb_kr")

    def cb_kl(self):
        print("cb_kl")

    def cb_km(self):
        print("cb_km")

    def cb_rtc(self, pin):
        print("rtc")
#         self.buzzer.set(1)
        pass

if __name__ == '__main__':
    try:
        horloge = WaveshareNixieClock()
        horloge.afficheurs[0].setLedColor(128, 0, 255)
        w = 135
        h = 10
        buffer = bytearray(w * h * 2)

        import framebuf
        class Test(framebuf.FrameBuffer):
            def __init__(self, buffer, width, height):
                super().__init__(buffer, width, height, framebuf.RGB565)
            
        test = Test(buffer, w, h)
    #     test.fill(0xffff)
        test.text("coucou", 0, 0, 0x0f0f)
        state = machine.disable_irq()
        try:
            horloge.afficheurs[0].show(0, 0, w, h, buffer)
        finally:
            machine.enable_irq(state)
        time.sleep(60)
    except KeyboardInterrupt:
        sys.exit()
