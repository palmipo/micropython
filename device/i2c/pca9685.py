from devicei2c import DeviceI2C

class PCA9685(DeviceI2C):
    
    def __init__(self, adresse, i2c):
        super().__init__(0x40 | (adresse & 0x07), i2c)
        
    def mode1(self, restart, extclk, ai, sleep, sub1addr=0, sub2addr=0, sub3addr=0, allcalladdr=0):
        cmd = arraybyte(2)
        cmd[0] = 0x00
        cmd[1] = (restart & 0x01) << 7
        cmd[1] |= (extclk & 0x01) << 6
        cmd[1] |= (ai & 0x01) << 5
        cmd[1] |= (sleep & 0x01) << 4
        cmd[1] |= (sub1addr & 0x01) << 3
        cmd[1] |= (sub2addr & 0x01) << 2
        cmd[1] |= (sub3addr & 0x01) << 1
        cmd[1] |= (allcalladdr & 0x01)
        self.busi2c.send(self.adresse, cmd)

        if sub1addr != 0:
            cmd = arraybyte(2)
            cmd[0] = 0x02
            cmd[1] = sub1addr
            self.busi2c.send(self.adresse, cmd)

        if sub2addr != 0:
            cmd = arraybyte(2)
            cmd[0] = 0x03
            cmd[1] = sub2addr
            self.busi2c.send(self.adresse, cmd)

        if sub3addr != 0:
            cmd = arraybyte(2)
            cmd[0] = 0x04
            cmd[1] = sub3addr
            self.busi2c.send(self.adresse, cmd)

        if allsubaddr != 0:
            cmd = arraybyte(2)
            cmd[0] = 0x05
            cmd[1] = allsubaddr
            self.busi2c.send(self.adresse, cmd)

    def mode2(self, invrt, och, outdrv, outne):
        cmd = arraybyte(2)
        cmd[0] = 0x01
        cmd[1] = (invrt & 0x01) << 4
        cmd[1] |= (och & 0x01) << 3
        cmd[1] |= (outdrv & 0x01) << 2
        cmd[1] |= (outne & 0x03)
        self.busi2c.send(self.adresse, cmd)

    def led(self, num, pourcent):
        valeur = pourcent * 4096 / 100
        self.led(num, valeur, 4096-valeur)

    # ON = 4096
    # OFF = 4096
    def led(self, num, on, off):
        cmd = arraybyte(5)
        cmd[0] = 0x06 + num * 4
        cmd[1] = on & 0x00ff
        cmd[2] = (on & 0x1f00) >> 8
        cmd[3] = off & 0x00ff
        cmd[4] = (off & 0x1f00) >> 8
        self.busi2c.send(self.adresse, cmd)

    def allLed(self, num, on, off):
        cmd = arraybyte(5)
        cmd[0] = 0xfa
        cmd[1] = on & 0x00ff
        cmd[2] = (on & 0x1f00) >> 8
        cmd[3] = off & 0x00ff
        cmd[4] = (off & 0x1f00) >> 8
        self.busi2c.send(self.adresse, cmd)

    def prescale(self, valeur):
        cmd = arraybyte(2)
        cmd[0] = 0xfe
        cmd[1] = valeur & 0xff
        self.busi2c.send(self.adresse, cmd)
