from device.spi.gc9a01a import GC9A01A
import time

class LCD_1inch28(GC9A01A):
    def __init__(self, dc, rst, cs, spi, pwm):

        self.dc = dc
        self.rst = rst
        self.cs = cs
        self.spi = spi
        self.pwm = pwm

#         self.cs(1)
#         self.dc(1)

        super().__init__()

        self.pwm.freq(5000)
    
    def set_bl_pwm(self, duty):
        self.pwm.duty_u16(duty)#max 65535

    def reset(self):
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
            
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def write_buffer(self, buffer):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buffer)
        self.cs(1)
