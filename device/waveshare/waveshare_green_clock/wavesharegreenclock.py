from wavesharegreenclockapps import WaveshareGreenClockApps
from sm5166 import SM5166P
from sm16106 import SM16106SC
from i2cpico import I2CPico
from ds3231_sqw import DS3231_SQW
from ds3231 import DS3231
import micropython
import machine

micropython.alloc_emergency_exception_buf(100)

class WaveshareGreenClock:
    def __init__(self):

        self.row = SM5166P(16, 18, 22)
        self.column = SM16106SC(10, 11, 12, 13)
        self.column.OutputEnable()
        
        self.i2c = I2CPico(1, 6, 7)
        # self.rtc = DS3231(0, self.i2c)
        self.rtc = DS3231_SQW(0, self.i2c, 3, self.callback_rtc)
        self.rtc.setControlRegister(0x01, 0x00, 0x00, 0x00, 0x00)
        self.rtc_beat = False

        self.K0 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
        self.K0.irq(handler=self.K0_callback, trigger=machine.Pin.IRQ_FALLING, hard=True)
        self.K0_click = False

        self.K1 = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
        self.K1.irq(handler=self.K1_callback, trigger=machine.Pin.IRQ_FALLING, hard=True)
        self.K1_click = False

        self.K2 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
        self.K2.irq(handler=self.K2_callback, trigger=machine.Pin.IRQ_FALLING, hard=True)
        self.K2_click = False

        self.buzzer = machine.Pin(14, machine.Pin.OUT)

    def K0_callback(self, pin):
        state = machine.disable_irq()
        try:
            self.K0_click = True
        finally:
            machine.enable_irq(state)

    def K1_callback(self, pin):
        state = machine.disable_irq()
        try:
            self.K1_click = True
        finally:
            machine.enable_irq(state)

    def K2_callback(self, pin):
        state = machine.disable_irq()
        try:
            self.K2_click = True
        finally:
            machine.enable_irq(state)

    def callback_rtc(self, pin):
        self.rtc_beat = True

    def is_k0_beat(self):
        if self.K0_click:
            self.K0_click = False
            return True
        else:
            return False

    def is_k1_beat(self):
        if self.K1_click:
            self.K1_click = False
            return True
        else:
            return False

    def is_k2_beat(self):
        if self.K2_click:
            self.K2_click = False
            return True
        else:
            return False

    def is_rtc_beat(self):
        if self.rtc_beat:
            self.rtc_beat = False
            return True
        else:
            return False

    # matrice de 4 * 8 bits
    def show(self, buffer):
        for i in range(8):
            self.column.send(buffer[i*4 : i*4+4])
            self.row.setChannel(i)
            self.column.latch()
