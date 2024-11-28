from device.spi.st7789v2 import ST7789V2

class Lcd_1inch69(ST7789V2):
    def __init__(self, dc, cs, rst, br, spi):
        self.dc = dc
        self.cs = cs
        self.rst = rst
        self.spi = spi
        self.pwm = br
        self.pwm.freq(50)
        self.pwm.duty_u16(50)
        self.rst(1)
        self.cs(1)
        self.dc(1)
        super().__init__()

    def write_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        data = bytearray(1)
        data[0] = cmd
        self.spi.write(data)
        self.cs(1)

    def write_data(self, buf):
        self.dc(1)
        self.cs(0)
        data = bytearray(1)
        data[0] = buf
        self.spi.write(data)
        self.cs(1)

    def write_buffer(self, buffer):
        self.dc(1)
        self.cs(0)
        self.spi.write(buffer)
        self.cs(1)

    def reset(self):
        self.rst(0)
        self.rst(1)

    def write_brightness(self, val):
        self.pwm.duty_u16(val)
