from devicei2c import DeviceI2C
import framebuf

class ScrollPHatHd(framebuf.FrameBuffer):
    def __init__(self, matrice):
        self.width = 17
        self.height = 7
        self.pages = 8
        self.matrice = matrice
        self.buffer = bytearray(self.width * self.height)
        super().__init__(self.buffer, self.width, self.height, framebuf.GS8)

    def show(self):
        self.matrice.pwmRegister(buffer)

class IS31FL3731(DeviceI2C):

    def __init__(self, address, bus):
        super().__init__(0x74 | (address & 0x03), bus)

    def frameRegister(self, page, led, blink, pwm):
        self.pageRegister(page)
        self.ledRegister(led)
        self.blinkRegister(blink)
        self.pwmRegister(pwm)
    
    def pageRegister(self, page):
        buf = bytearray(2)
        buf[0] = 0xfd
        buf[1] = page & 0x07
        self.busi2c.send(self.adresse, buf)

    def ledRegister(self, led):
        data1 = bytearray(19)
        data1[0] = 0x00
        data1[1:] = led
        self.busi2c.send(self.adresse, data1)

    def blinkRegister(self, blink):
        data1 = bytearray(19)
        data1[0] = 0x19
        data1[1:] = blink
        self.busi2c.send(self.adresse, data1)

    def pwmRegister(self, pwm):
        data2 = bytearray(145)
        data2[0] = 0x24
        data2[1:] = pwm
        self.busi2c.send(self.adresse, data2)

    def configurationRegister(self, mode, fs):
        buf = bytearray(2)
        buf[0] = 0xfd
        buf[1] = 0x0b
        self.busi2c.send(self.adresse, buf)
        
        buf[0] = 0x00
        buf[1] = ((mode & 0x3) << 3) | (fs & 0x7)
        self.busi2c.send(self.adresse, buf)

    def pictureDisplayRegister(self, pfs):
        buf = bytearray(2)
        buf[0] = 0xfd
        buf[1] = 0x0b
        self.busi2c.send(self.adresse, buf)
        
        buf[0] = 0x01
        buf[1] = (pfs & 0x7)
        self.busi2c.send(self.adresse, buf)
        
    def autoplayControlRegister(self, cns, fns, fdt):
        buf = bytearray(2)
        buf[0] = 0xfd
        buf[1] = 0x0b
        self.busi2c.send(self.adresse, buf)

        data = bytearray(3)
        data[0] = 0x02
        data[1] = ((cns & 0x7) << 4) | (fns & 0x7)
        data[2] = (fdt & 0x3f)
        self.busi2c.send(self.adresse, data)

    def displayOptionRegister(self, ic, be, bpt):
        buf = bytearray(2)
        buf[0] = 0xfd
        buf[1] = 0x0b
        self.busi2c.send(self.adresse, buf)
        
        buf[0] = 0x05
        buf[1] = ((ic & 0x1) << 5) | ((be & 0x1) << 3) | (bpt & 0x7)
        self.busi2c.send(self.adresse, buf)
        
    def breathControlRegister(self, b_en, fot, fit, et):
        buf = bytearray(2)
        buf[0] = 0xfd
        buf[1] = 0x0b
        self.busi2c.send(self.adresse, buf)

        data = bytearray(3)
        data[0] = 0x08
        data[1] = ((fot & 0x7) << 4) | (fit & 0x7)
        data[2] = ((b_en & 0x1) << 4) | (et & 0x7)
        self.busi2c.send(self.adresse, data)

    def shutdown(self, on):
        buf = bytearray(2)
        buf[0] = 0xfd
        buf[1] = 0x0b
        self.busi2c.send(self.adresse, buf)
        
        buf[0] = 0x0a
        buf[1] = on & 0x01
        self.busi2c.send(self.adresse, buf)
