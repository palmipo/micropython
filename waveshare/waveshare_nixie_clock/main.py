import time
from machine import Pin
from neopixel import NeoPixel
from master.net.wlanpico import WLanPico
from master.i2c.i2cpico import I2CPico
# from device.i2c.ds3231 import DS3231
from device.i2c.ds3231_sqw import DS3231_SQW
import sys
from device.afficheur.lcd_1inch14 import Lcd_1inch14
from master.pia.piapico import PiaPicoOutput, PiaPicoInput
from master.pwm.pwmpico import PwmPico
from device.waveshare.waveshare_nixie_clock.spipiconixie import SPIPicoNixie

class WaveshareNixieClock:
    def __init__(self):
        self.wlan = WLanPico()
        self.wlan.connect()

        self.kr = PiaPicoInput(15, self.cb_kr)
        self.kl = PiaPicoInput(16, self.cb_kl)
        self.km = PiaPicoInput(17, self.cb_km)
#         self.buzzer = PwmPico(14)

        self.i2c = I2CPico(1, 6, 7)
#         self.bme280 = BME280(self.i2c)
        self.ds1321 = DS3231_SQW(0, self.i2c, 18, self.cb_rtc)
        self.ds1321.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)

        rst = PiaPicoOutput(12)
        rst.set(1)
        
        spi = SPIPicoNixie()
        
        dc = PiaPicoOutput(8)
        dc.set(1)
        
        bl = PwmPico(13)
        led = NeoPixel(Pin(22, Pin.OUT), 6)

        for num in range (0,6):
            self.LCD = Lcd_1inch14(num, dc, rst, spi, bl, led)

 
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

if __name__ == '__main__':
    try:
        horloge = WaveshareNixieClock()

        buffer = bytearray(horloge.LCD.width * horloge.LCD.height * 2)

        import framebuf            
        test = framebuf.FrameBuffer(buffer, horloge.LCD.width, horloge.LCD.height, framebuf.RGB565)

        for num in range (0,6):
            horloge.LCD.setLedColor(num, 0x80, 0, 0xff)
            test.fill(0x00ffffff)
            test.text("Hello World {}".format(num), 0, 0)
            horloge.LCD.show(num, 0, 0, horloge.LCD.width, horloge.LCD.height, buffer)

        time.sleep(10)
    except KeyboardInterrupt:
        pass
