from master.i2c.i2cpico import I2CPico
from device.i2c.ds3231_sqw import DS3231_SQW
from master.pia.piapico import PiaOutputPico
from master.pia.piaisrbouncepico import PiaIsrBouncePico
from master.pwm.pwmpico import PwmPico
from waveshare.waveshare_nixie_clock.nixielcd import NixieLcd
import time

class NixieClock:
    def __init__(self):
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

    def scrute(self):
        if self.kr.isActivated() == True:
            self.buzzer.setFrequency(50000)
            self.buzzer.setDuty(99)
            time.sleep_ms(50)
            self.buzzer.setDuty(0)

        if self.kl.isActivated() == True:
            self.buzzer.setFrequency(80000)
            self.buzzer.setDuty(99)
            time.sleep_ms(50)
            self.buzzer.setDuty(0)

        if self.km.isActivated() == True:
            self.buzzer.setFrequency(20000)
            self.buzzer.setDuty(99)
            time.sleep_ms(50)
            self.buzzer.setDuty(0)

        if self.ds1321.isActivated() == True:
            self.buzzer.setFrequency(10000)
            self.buzzer.setDuty(99)
            time.sleep_ms(10)
            self.buzzer.setDuty(0)

# nixie = NixieClock()
# while True:
#     nixie.scrute()
#     time.sleep_ms(100)
