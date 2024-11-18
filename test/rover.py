import rp2
import machine
from master.i2c.i2cpico import I2CPico 
from device.i2c.pca9685 import PCA9685

try:
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
