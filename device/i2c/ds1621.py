from devicei2c import DeviceI2C

class DS1621(DeviceI2C):

    def __init__(self, address, bus):
        super().__init__(0x48 | (address & 0x03), bus)

    def getAccessTh(self):
        buf = bytearray(1)
        buf[0] = 0xa1
        return self.busi2c.transferer(self.adresse, buf)

    def setAccessTh(self, valeur):
        buf = bytearray(3)
        buf[0] = 0xa1
        buf[1] = ((1<<8) + valeur) & 0xff
        buf[2] = 0
        self.busi2c.send(self.adresse, buf)
        time.sleep_ms(10)

    def getAccessTl(self):
        buf = bytearray(1)
        buf[0] = 0xa2
        return self.busi2c.transferer(self.adresse, buf)

    def setAccessTl(self, valeur):
        buf = bytearray(3)
        buf[0] = 0xa2
        buf[1] = ((1<<8) + valeur) & 0xff
        buf[2] = 0
        self.busi2c.send(self.adresse, buf)
        time.sleep_ms(10)

    def readOneTemperature(self):
        buf = bytearray(1)
        buf[0] = 0xaa
        return self.busi2c.transferer(self.adresse, buf, 2)

    def start(self):
        buf = bytearray(1)
        buf[0] = 0xee
        return self.busi2c.send(self.adresse, buf, 1)
        
    def stop(self):
        buf = bytearray(1)
        buf[0] = 0x22
        return self.busi2c.send(self.adresse, buf, 1)
        
    def readTemperature(self):
        slope = readSlope()
        counter = readCounter()

        buf = bytearray(1)
        buf[0] = 0xaa
        msg = self.busi2c.transferer(self.adresse, buf, 2)

        t = float((1<<8) - msg[0])
        if msg[1] != 0:
            t += 0.5
        return (t + ((slope - counter) / slope))

    def readCounter(self):
        buf = bytearray(1)
        buf[0] = 0xa8
        return self.busi2c.transferer(self.adresse, buf, 1)

    def readSlope(self):
        buf = bytearray(1)
        buf[0] = 0xa9
        return self.busi2c.transferer(self.adresse, buf, 1)
        
    def read(self):
        waitDone()

        buf = bytearray(1)
        buf[0] = 0xa8
        msg = self.busi2c.transferer(self.adresse, buf, 4)
        counter = float(msg[0])
        slope = float(msg[1])
        t = float((1<<8) - msg[2])
        if msg[3] != 0:
            t += 0.5
        return (t + ((slope - counter) / slope))

    def waitDone(self):
        buf = bytearray(1)
        buf[0] = 0xac
        access_config = self.busi2c.transferer(self.adresse, buf, 1)
        while (access_config & 0x80) == 0:
            access_config = self.busi2c.transferer(self.adresse, buf, 1)

    def waitNVB(self):
        buf = bytearray(1)
        buf[0] = 0xac
        access_config = self.busi2c.transferer(self.adresse, buf, 1)
        while (access_config & 0x10) == 0:
            access_config = self.busi2c.transferer(self.adresse, buf, 1)
