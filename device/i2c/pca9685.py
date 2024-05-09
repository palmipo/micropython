from devicei2c import DeviceI2C
import time

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
    def mode1(self, freq, subaddr1=0, subaddr2=0, subaddr3=0, allcalladdr=0):
        cmd = bytearray(2)
        cmd[0] = 0x00
        cmd[1] = 1 << 5 # auto increment

        if subaddr1 != 0:
            cmd[1] |= 0x01 << 3
            addr1 = bytearray(2)
            addr1[0] = 0x02
            addr1[1] = (subaddr1 & 0x7f) << 1
            self.busi2c.send(self.adresse, addr1)

        if subaddr2 != 0:
            cmd[1] |= 0x01 << 2
            addr2 = bytearray(2)
            addr2[0] = 0x03
            addr2[1] = (subaddr2 & 0x7F) << 1
            self.busi2c.send(self.adresse, addr2)

        if subaddr3 != 0:
            cmd[1] |= 0x01 << 1
            addr3 = bytearray(2)
            addr3[0] = 0x04
            addr3[1] = (subaddr3 & 0x7f) << 1
            self.busi2c.send(self.adresse, addr3)

        if allcalladdr != 0:
            cmd[1] |= 0x01
            addr4 = bytearray(2)
            addr4[0] = 0x05
            addr4[1] = (allcalladdr & 0x7f) << 1
            self.busi2c.send(self.adresse, addr4)

        # sleep = 1 pour ecriture du prescaler
        sleep = bytearray(2)
        sleep[0] = 0
        sleep[1] = cmd[1] | (1 << 4)
        self.busi2c.send(self.adresse, sleep)
        time.sleep_ms(1)

        prescaler = 25000000
        prescaler //= 4096
        prescaler *= freq
        prescaler -= 1
        print(int(prescaler))
        if (prescaler >= 0x03):
            # ecriture de la valeur du prescaler
            scl = bytearray(2)
            scl[0] = 0xfe
            scl[1] = int(prescaler)
            self.busi2c.send(self.adresse, scl)

        self.busi2c.send(self.adresse, cmd)
        time.sleep_ms(1)

    def mode2(self, invrt, och, outdrv, outne):
        cmd = bytearray(2)
        cmd[0] = 0x01
        cmd[1] = (invrt & 0x01) << 4
        cmd[1] |= (och & 0x01) << 3
        cmd[1] |= (outdrv & 0x01) << 2
        cmd[1] |= (outne & 0x03)
        self.busi2c.send(self.adresse, cmd)

    # ON = 4096
    # OFF = 0
    def led(self, num, on, off):
        cmd = bytearray(5)
        cmd[0] = 0x06 + num * 4
        cmd[1] = off & 0x00ff
        cmd[2] = (off & 0x0f00) >> 8
        cmd[3] = on & 0x00ff
        cmd[4] = (on & 0x0f00) >> 8
        self.busi2c.send(self.adresse, cmd)

    def ledOn(self, num):
        cmd = bytearray(5)
        cmd[0] = 0x06 + num * 4
        cmd[1] = 0
        cmd[2] = 1 << 4
        cmd[3] = 0
        cmd[4] = 0
        self.busi2c.send(self.adresse, cmd)

    def ledOff(self, num):
        cmd = bytearray(5)
        cmd[0] = 0x06 + num * 4
        cmd[1] = 0
        cmd[2] = 0
        cmd[3] = 0
        cmd[4] = 1 << 4
        self.busi2c.send(self.adresse, cmd)

    def allLed(self, on, off):
        cmd = bytearray(5)
        cmd[0] = 0xfa
        cmd[1] = off & 0x00ff
        cmd[2] = (off & 0x0f00) >> 8
        cmd[3] = on & 0x00ff
        cmd[4] = (on & 0x0f00) >> 8
        self.busi2c.send(self.adresse, cmd)

    def allLedOn(self):
        cmd = bytearray(5)
        cmd[0] = 0xfa
        cmd[1] = 0
        cmd[2] = 1 << 4
        cmd[3] = 0
        cmd[4] = 0
        self.busi2c.send(self.adresse, cmd)

    def allLedOff(self):
        cmd = bytearray(5)
        cmd[0] = 0xfa
        cmd[1] = 0
        cmd[2] = 0
        cmd[3] = 0
        cmd[4] = 1 << 4
        self.busi2c.send(self.adresse, cmd)

if __name__ == '__main__':
    try:
        import rp2
        import machine
        from i2cpico import I2CPico
        i2c = I2CPico(0, 20, 21)
        try:
            pca9685 = PCA9685(0, i2c)
            pca9685.mode1(50000000)


            class Motor:
                def __init__(self, num, pca9685):
                    self.num = num
                    self.pca9685 = pca9685

                def stop(self, speed):
                        self.pca9685.led(self.num, speed, 0)
                        self.pca9685.ledOff(self.num+1)
                        self.pca9685.ledOff(self.num+2)

                def forward(self, speed):
                        self.pca9685.led(self.num, speed, 0)
                        self.pca9685.ledOn(self.num+1)
                        self.pca9685.ledOff(self.num+2)
                    
                def revert(self, speed):
                        self.pca9685.led(self.num, speed, 0)
                        self.pca9685.ledOff(self.num+1)
                        self.pca9685.ledOn(self.num+2)
                    
                def block(self, speed):
                        self.pca9685.led(self.num, speed, 0)
                        self.pca9685.ledOn(self.num+1)
                        self.pca9685.ledOn(self.num+2)

            class Chenille:
                def __init__(self, moteur1, moteur2):
                    self.m1 = moteur1
                    self.m2 = moteur2

                def stop(self):
                    self.m1.stop()
                    self.m2.stop()

                def forward(self, speed):
                    self.m1.forward(speed)
                    self.m2.revert(speed)

                def revert(self, speed):
                    self.m1.revert(speed)
                    self.m2.forward(speed)

            # chenille droite
            moteur1 = Motor(0, pca9685)
            moteur2 = Motor(3, pca9685)
            chenilleD = Chenille(moteur1, moteur2)
            chenilleD.forward(0xfff)

            # chenille gauche
            moteur3 = Motor(6, pca9685)
            moteur4 = Motor(9, pca9685)
            chenilleG = Chenille(moteur3, moteur4)
            chenilleG.forward(0xfff)
    
            time.sleep(2)
        finally:
            pca9685.allLedOff()
            print("FIN.")

    except KeyboardInterrupt:
        print("quit")
        sys.exit()
