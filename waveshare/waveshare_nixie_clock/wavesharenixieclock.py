from master.i2c.i2cpico import I2CPico
from device.i2c.ds3231_sqw import DS3231_SQW
from master.pia.piapico import PiaOutputPico
from master.pia.piaisrpico import PiaIsrPico
from master.pwm.pwmpico import PwmPico
from waveshare.waveshare_nixie_clock.nixielcd import NixieLcd

class WaveshareNixieClock:
    def __init__(self):
        self.kr = PiaIsrPico(15)
        self.kl = PiaIsrPico(16)
        self.km = PiaIsrPico(17)
        self.buzzer = PwmPico(14)

        self.i2c = I2CPico(1, 6, 7)
#         self.bme280 = BME280(self.i2c)
        self.ds1321 = DS3231_SQW(0, self.i2c, 18)
        self.ds1321.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)


        self.nixie = NixieLcd(rst_pin = 12, dc_pin = 8, bl_pin = 13, led_pin = 22)

    def scrute(self):
        if self.kr.isActivated():
            print("cb_kr")

        if self.kl.isActivated():
            print("cb_kl")

        if self.km.isActivated():
            print("cb_km")

        if self.ds1321.isActivated():
            print("rtc")

import time
nixie = WaveshareNixieClock()
nixie.buzzer.setDuty(100)
time.sleep(2)
