from master.net.wlanpico import WLanPico
from device.net.ntp import Ntp
from master.i2c.i2cpico import I2CPico
from device.i2c.bmp280 import BMP280
from device.i2c.ds3231_sqw import DS3231_SQW
from master.pwm.pwmpico import PwmPico
from master.pia.piaisrbouncepico import PiaIsrBouncePico
from waveshare.waveshare_nixie_clock.nixielcd import NixieLcd
import framebuf, time, machine, rp2

class NixieClock:
    def __init__(self):
        self.wlan = WLanPico()
        self.wlan.connect()
        
        ntp = Ntp()
        ntp.ntp()

        self.kr = PiaIsrBouncePico(15, pullUp=machine.Pin.PULL_DOWN, trigger=machine.Pin.IRQ_FALLING)
        self.kl = PiaIsrBouncePico(16, pullUp=machine.Pin.PULL_DOWN, trigger=machine.Pin.IRQ_FALLING)
        self.km = PiaIsrBouncePico(17, pullUp=machine.Pin.PULL_DOWN, trigger=machine.Pin.IRQ_FALLING)
        self.buzzer = PwmPico(14)
        self.buzzer.setFrequency(50)

        self.i2c = I2CPico(1, 6, 7)

        self.bmp280 = BMP280(self.i2c)
        self.bmp280.reset()
        time.sleep(1)
        print("chipIdRegister {}".format(self.bmp280.chipIdRegister()))
        # osrs_t x2  : 010b
        # osrs_p x16 : 101b
        # mode       : normal 11b
        self.bmp280.ctrlMeasureRegister(osrs_t=2, osrs_p=5, mode=3)
        # t_sb   3
        # filtre 16
        self.bmp280.configRegister(t_sb=3, filtre=16)

        self.ds1321 = DS3231_SQW(0, self.i2c, 18)
        self.ds1321.setAlarm1(A1M=0x0F, hour='08:00:00', day='03')
        self.ds1321.setControlRegister(CONV=0x01, RS=0x00, INTCN=0x00, A2IE=0x00, A1IE=0x01, EN32kHz=0)

        self.nixie = NixieLcd(rst_pin = 12, dc_pin = 8, bl_pin = 13, led_pin = 22)
        self.buffer = bytearray(self.nixie.LCDs[0].width * self.nixie.LCDs[0].height * 2)
        self.dessin = framebuf.FrameBuffer(self.buffer, self.nixie.LCDs[0].width, self.nixie.LCDs[0].height, framebuf.RGB565)    

        self.clear()

    def clear(self):
        for num in range(len(self.nixie.LCDs)):
            self.dessin.fill(0)
            self.nixie.LCDs[num].show(0, 0, self.nixie.LCDs[num].width, self.nixie.LCDs[num].height, self.buffer)
