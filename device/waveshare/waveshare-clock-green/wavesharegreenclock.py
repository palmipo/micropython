from sm5166 import SM5166P
from sm16106 import SM16106SC
from i2cpico import I2CPico
from ds3231_sqw import DS3231_SQW
from ds3231 import DS3231
import micropython
import machine

micropython.alloc_emergency_exception_buf(100)

class WaveshareGreenClock:
    def __init__(self, app):
        self.app = app
        
        self.row = SM5166P(16, 18, 22)
        self.column = SM16106SC(10, 11, 12, 13)
        self.column.OutputEnable()
        
        self.i2c = I2CPico(1, 6, 7)
        if self.app.cb_rtc != None:
            self.rtc = DS3231_SQW(0, self.i2c, 3, self.callback_rtc)
            self.rtc.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)
        else:
            self.rtc = DS3231(0, self.i2c)

        self.K0 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
        if self.app.cb_down != None:
            self.K0.irq(handler=self.callback_down, trigger=machine.Pin.IRQ_FALLING, hard=True)

        self.K1 = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
        if self.app.cb_center != None:
            self.K1.irq(handler=self.callback, trigger=machine.Pin.IRQ_FALLING, hard=True)
        
        self.K2 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
        if self.app.cb_up != None:
            self.K2.irq(handler=self.callback_up, trigger=machine.Pin.IRQ_FALLING, hard=True)
        
        self.buzzer = machine.Pin(14, machine.Pin.OUT)

    def callback(self, pin):
        state = machine.disable_irq()
        try:
            if self.app.cb_center != None:
                self.app.cb_center()
        finally:
            machine.enable_irq(state)

    def callback_up(self, pin):
        state = machine.disable_irq()
        try:
            if self.app.cb_up != None:
                self.app.cb_up()
        finally:
            machine.enable_irq(state)

    def callback_down(self, pin):
        state = machine.disable_irq()
        try:
            if self.app.cb_down != None:
                self.app.cb_down()
        finally:
            machine.enable_irq(state)

    def callback_rtc(self, pin):
        if self.app.cb_rtc != None:
            self.app.cb_rtc()

    # matrice de 4 * 8 bits
    def show(self, buffer):
        for i in range(8):
            self.column.send(buffer[i*4 : i*4+4])
            self.row.setChannel(i)
            self.column.latch()
