from master.net.wlanpico import WLanPico
from master.i2c.i2cpico import I2CPico
from device.i2c.ds3231_sqw import DS3231_SQW
from master.pwm.pwmpico import PwmPico
from master.pia.piaisrbouncepico import PiaIsrBouncePico
from waveshare.waveshare_nixie_clock.nixielcd import NixieLcd
import framebuf

class NixieClock:
    def __init__(self):
        self.wlan = WLanPico()
        self.wlan.connect()

        self.kr = PiaIsrBouncePico(15)
        self.kl = PiaIsrBouncePico(16)
        self.km = PiaIsrBouncePico(17)
        self.buzzer = PwmPico(14)
        self.buzzer.setFrequency(50)

        self.i2c = I2CPico(1, 6, 7)
#         self.bme280 = BME280(self.i2c)
        self.ds1321 = DS3231_SQW(0, self.i2c, 18)
        self.ds1321.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)

        self.nixie = NixieLcd(rst_pin = 12, dc_pin = 8, bl_pin = 13, led_pin = 22)
        self.buffer = bytearray(self.nixie.LCDs[0].width * self.nixie.LCDs[0].height * 2)
        self.dessin = framebuf.FrameBuffer(self.buffer, self.nixie.LCDs[0].width, self.nixie.LCDs[0].height, framebuf.RGB565)    

        for num in range(len(self.nixie.LCDs)):
            self.nixie.setLedColor(num, 0x80, 0, 0xff)
            self.dessin.fill(0x00ffffff)
            self.nixie.LCDs[num].show(0, 0, self.nixie.LCDs[num].width, self.nixie.LCDs[num].height, self.buffer)
