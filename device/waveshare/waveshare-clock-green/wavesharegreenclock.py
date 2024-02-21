from sm5166 import SM5166P
from sm16106 import SM16106SC
from i2cpico import I2CPico
from ds3231_sqw import DS3231_SQW
import micropython
import machine

micropython.alloc_emergency_exception_buf(100)

class WaveshareGreenClock:
    def __init__(self, cb_up = None, cb_center = None, cb_down = None, cb_rtc = None):
        self.cb_up = cb_up
        self.cb_center = cb_center
        self.cb_down = cb_down
        self.cb_rtc = cb_rtc
        
        self.row = SM5166P(16, 18, 22)
        self.column = SM16106SC(10, 11, 12, 13)
        
        self.i2c = I2CPico(1, 6, 7)
        if cb_rtc != None:
            self.rtc = DS3231_SQW(0, self.i2c, 3, self.callback_rtc)
            self.rtc.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)
        else:
            self.rtc = DS3231(0, self.i2c)

        self.K0 = PiaPicoInp(15, self.callback_down)

        self.K1 = PiaPicoInp(17, self.callback)
        
        self.K2 = PiaPicoInp(2, self.callback_up)
        
        self.buzzer = PiaPicoOut(14)

    def callback(self, pin):
        self.cb_center()

    def callback_up(self, pin):
        self.cb_up()

    def callback_down(self, pin):
        self.cb_down()

    def callback_rtc(self, pin):
        self.cb_rtc()

    # matrice de 4 * 8 bits
    def show(self, buffer):
        self.column.OutputEnable()
        for i in range(8):
            self.column.send(buffer[i*4 : i*4+4])
            self.row.setChannel(i)
            self.column.latch()
        self.column.OutputDisable()
