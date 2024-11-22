from waveshare.waveshare_green_clock.wavesharegreenclockapps import WaveshareGreenClockApps
from waveshare.waveshare_green_clock.sm5166p import SM5166P
from waveshare.waveshare_green_clock.sm16106sc import SM16106SC
from master.i2c.i2cpico import I2CPico
from device.i2c.ds3231_sqw import DS3231_SQW
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

    def is_k0_beat(self):
        if self.K0_click == True:
            self.K0_click = False
            return True
        else:
            return False

    def is_k1_beat(self):
        if self.K1_click == True:
            self.K1_click = False
            return True
        else:
            return False

    def is_k2_beat(self):
        if self.K2_click == True:
            self.K2_click = False
            return True
        else:
            return False

    def is_rtc_beat(self):
        return self.rtc.isActivated()

    # matrice de 4 * 8 bits
    def show(self, buffer):
        for i in range(8):
            self.column.send(buffer[i*4 : i*4+4])
            self.row.setChannel(i)
            self.column.latch()
