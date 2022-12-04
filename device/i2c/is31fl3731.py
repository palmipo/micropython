from devicei2c import DeviceI2C

class IS31FL3731(DeviceI2C):

    def __init__(self, address, bus):
        super().__init__(0x74 & (address & 0x03), bus)

    def frameRegister(self, page, led, blink, pwm):
        buf = bytearray(2)
        buf[0] = 0xfd
        buf[1] = page & 0x07
        self.busi2c.send(self.adresse, buf)

        data1 = bytearray(37)
        data1[0] = 0
        for i in range(0, 18):
            data1[i+1] = led[i]
            data1[i+19] = blink[i]
        self.busi2c.send(self.adresse, data1)

        data2 = bytearray(145)
        data2[0] = 0x24
        for i in range(0, 144):
            data2[i+1] = pwm[i]
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
