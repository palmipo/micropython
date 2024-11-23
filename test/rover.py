import rp2
import machine
from master.i2c.i2cpico import I2CPico 
from device.i2c.pca9685 import PCA9685

class Motor:
    def __init__(self, num, pca9685):
        pontH = L298N(PwmPca9685(num, pca9685), PiaPca9685(num+1, pca9685), PiaPca9685(num+2, pca9685))

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

try:
    i2c = I2CPico(0, 20, 21)
    pca9685 = PCA9685(0, i2c)
    pca9685.mode1(50000000)


    # chenille droite
    moteur1 = Motor(0, pca9685)
    moteur2 = Motor(3, pca9685)
    chenilleD = Chenille(moteur1, moteur2)

    # chenille gauche
    moteur3 = Motor(6, pca9685)
    moteur4 = Motor(9, pca9685)
    chenilleG = Chenille(moteur3, moteur4)

    chenilleD.forward(0xfff)
    chenilleG.forward(0xfff)

    time.sleep(2)

except KeyboardInterrupt:
    print("quit")

finally:
    pca9685.allLedOff()
    print("FIN.")
