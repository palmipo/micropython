from devicei2c import DeviceI2C

class PCA9685(DeviceI2C):
    
    def __init__(self, adresse, i2c):
        super().__init__(0x40 | (adresse & 0x07), i2c)
        
    # frequence interne maxi 25MHz
    # frequence externe maxi 50MHz
    # prescaler = (frequence maxi / (4096 x frequence)) - 1
    # subaddr1 = 0x71 (0xE2) par defaut
    # subaddr2 = 0x72 (0xE4) par defaut
    # subaddr3 = 0x74 (0xE8) par defaut
    # alladdrcall = 0x70 (0xE0) par defaut
    def mode1(self, freq, sub1addr=0, sub2addr=0, sub3addr=0, allcalladdr=0):
        cmd = arraybyte(2)
        cmd[0] = 0x00
        cmd[1] = 0x00
        cmd[1] |= 1 << 5 # auto increment

        if sub1addr != 0:
            cmd[1] |= 0x01 << 3
            addr = arraybyte(2)
            addr[0] = 0x02
            addr[1] = (sub1addr & 0x7f) << 1
            self.busi2c.send(self.adresse, addr)

        if sub2addr != 0:
            cmd[1] |= 0x01 << 2
            addr = arraybyte(2)
            addr[0] = 0x03
            addr[1] = (sub2addr & 0x7F) << 1
            self.busi2c.send(self.adresse, addr)

        if sub3addr != 0:
            cmd[1] |= 0x01 << 1
            addr = arraybyte(2)
            addr[0] = 0x04
            addr[1] = (sub3addr & 0x7f) << 1
            self.busi2c.send(self.adresse, addr)

        if allsubaddr != 0:
            cmd[1] |= 0x01
            addr = arraybyte(2)
            addr[0] = 0x05
            addr[1] = (allsubaddr & 0x7f) << 1
            self.busi2c.send(self.adresse, addr)

        # sleep = 1 pour ecriture du prescaler
        self.busi2c.send(self.adresse, cmd | (1 << 4))

        prescaler = (25000000 / (4096 x freq)) - 1
        if (prescaler >= 0x03):
            # ecriture de la valeur du prescaler
            scl = arraybyte(2)
            scl[0] = 0xfe
            scl[1] = prescaler & 0xff
            self.busi2c.send(self.adresse, scl)

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
        self.led(num, 0, valeur)

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
