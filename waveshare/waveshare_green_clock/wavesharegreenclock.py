from waveshare.waveshare_green_clock.wavesharegreenclockapps import WaveshareGreenClockApps
from waveshare.waveshare_green_clock.sm5166p import SM5166P
from waveshare.waveshare_green_clock.sm16106sc import SM16106SC
from master.i2c.i2cpico import I2CPico
from device.i2c.ds3231_sqw import DS3231_SQW
from master.pia.piapico import PiaOutputPico
from master.pia.piaisrpico import PiaIsrPico
import micropython
import machine

micropython.alloc_emergency_exception_buf(100)

class WaveshareGreenClock:
    def __init__(self):

        self.row = SM5166P(16, 18, 22)
        self.column = SM16106SC(10, 11, 12, 13)
        self.column.OutputEnable()
        
        self.i2c = I2CPico(1, 6, 7)
        self.rtc = DS3231_SQW(0, self.i2c, 3)
        self.rtc.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)

        self.K0 = PiaIsrPico(15)
        self.K1 = PiaIsrPico(17)
        self.K2 = PiaIsrPico(2)

        self.buzzer = PiaOutputPico(14)

    def is_k0_beat(self):
        return self.K0.isActivated()

    def is_k1_beat(self):
        return self.K1.isActivated()

    def is_k2_beat(self):
        return self.K2.isActivated()

    def is_rtc_beat(self):
        return self.rtc.isActivated()

    # matrice de 4 * 8 bits
    def show(self, buffer):
        for i in range(8):
            self.column.send(buffer[i*4 : i*4+4])
            self.row.setChannel(i)
            self.column.latch()
