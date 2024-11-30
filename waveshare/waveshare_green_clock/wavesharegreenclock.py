from waveshare.waveshare_green_clock.wavesharegreenclockascii import WaveshareGreenClockAscii4x7
from waveshare.waveshare_green_clock.wavesharegreenclockascii import WaveshareGreenClockAscii5x7
from waveshare.waveshare_green_clock.wavesharegreenclockcodec import WaveshareGreenClockCodec
from waveshare.waveshare_green_clock.wavesharegreenclocktag import WaveshareGreenClockTag
from waveshare.waveshare_green_clock.sm5166p import SM5166P
from waveshare.waveshare_green_clock.sm16106sc import SM16106SC
from master.i2c.i2cpico import I2CPico
from device.i2c.ds3231_sqw import DS3231_SQW
from master.pwm.pwmpico import PwmPico
from master.pia.piaisrpico import PiaIsrPico
from master.net.wlanpico import WLanPico
from device.net.ntp import Ntp
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
        self.rtc.setControlRegister(CONV=1, RS=0, INTCN=0x00, A2IE=0, A1IE=0, EN32kHz=0)

        self.K0 = PiaIsrPico(15, pullUp=machine.Pin.PULL_UP)
        self.K1 = PiaIsrPico(17, pullUp=machine.Pin.PULL_UP)
        self.K2 = PiaIsrPico(2, pullUp=machine.Pin.PULL_UP)

        self.buzzer = PwmPico(14)

        self.buffer = bytearray(4*8)
        self.codec = WaveshareGreenClockCodec()
        self.ascii = WaveshareGreenClockAscii4x7()
        self.tag = WaveshareGreenClockTag(self.buffer)

        try:
            self.wlan = WLanPico()
            self.wlan.connect()
            
            ntp = Ntp()
            data_tuple = ntp.ntp()

            laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
            lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])

            self.rtc.setDate(laDate)
            self.rtc.setDayWeek(str(data_tuple[6]))
            self.rtc.setTime(lHeure)
        except OSError:
            pass
        finally:
            self.wlan.disconnect()

    # matrice de 4 * 8 bits
    def show(self, buffer):
        for i in range(8):
            self.column.send(buffer[i*4 : i*4+4])
            self.row.setChannel(i)
            self.column.latch()
