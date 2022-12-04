from devicei2c import DeviceI2C
import time

class DS1621(DeviceI2C):

    def __init__(self, address, bus):
        super().__init__(0x48 | (address & 0x03), bus)

    def getAccess(self):
        buf = bytearray(1)
        buf[0] = 0xa1
        msg = self.busi2c.transferer(self.adresse, buf, 4)
        th = (1<<8) - msg[0]
        tl = (1<<8) - msg[2]
        return th, tl

    def setAccess(self, th, tl):
        buf = bytearray(5)
        buf[0] = 0xa1
        buf[1] = (1<<8) + (th & 0xff)
        buf[2] = 0
        buf[3] = (1<<8) + (tl & 0xff)
        buf[4] = 0
        self.busi2c.send(self.adresse, buf)
        time.sleep_ms(10)
        self.waitNVB()

    def isThf(self):
        cmd = bytearray(1)
        cmd[0] = 0xac
        buf = self.busi2c.transferer(self.adresse, cmd, 1)
        return ((((buf[0] & 0x40) >> 6) != 0) ? True : False)

    def isTlf(self):
        cmd = bytearray(1)
        cmd[0] = 0xac
        buf = self.busi2c.transferer(self.adresse, cmd, 1)
        return ((((buf[0] & 0x20) >> 5) != 0) ? True : False)

    def readOneTemperature(self):
        cmd = bytearray(2)
        cmd[0] = 0xac
        cmd[1] = 0x01
        self.busi2c.send(self.adresse, cmd)

        time.sleep_ms(10)
        self.waitNVB()

        self.start()
        return self.readTemperature()

    def start(self):
        buf = bytearray(1)
        buf[0] = 0xee
        return self.busi2c.send(self.adresse, buf, 1)
        
    def stop(self):
        buf = bytearray(1)
        buf[0] = 0x22
        return self.busi2c.send(self.adresse, buf, 1)
        
    def readTemperature(self):
        self.waitDone()

        slope = self.readSlope()
        counter = self.readCounter()

        buf = bytearray(1)
        buf[0] = 0xaa
        msg = self.busi2c.transferer(self.adresse, buf, 2)

        t = (1<<8) - msg[0]
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
        self.waitDone()

        buf = bytearray(1)
        buf[0] = 0xa8
        msg = self.busi2c.transferer(self.adresse, buf, 4)

        counter = float(msg[0])
        slope = float(msg[1])
        t = (1<<8) - msg[2]
        return (t + ((slope - counter) / slope))

    def waitDone(self):
        buf = bytearray(1)
        buf[0] = 0xac
        access_config = self.busi2c.transferer(self.adresse, buf, 1)
        while (access_config & 0x80) == 0:
            time.sleep_ms(1)
            access_config = self.busi2c.transferer(self.adresse, buf, 1)

    def waitNVB(self):
        buf = bytearray(1)
        buf[0] = 0xac
        access_config = self.busi2c.transferer(self.adresse, buf, 1)
        while (access_config & 0x10) == 0:
            time.sleep_ms(1)
            access_config = self.busi2c.transferer(self.adresse, buf, 1)
