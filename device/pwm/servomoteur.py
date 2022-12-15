from pca9685 import PCA9685

class ServoMoteur:
    def __init__(self, voie, pca9685)
        self.voie = voie
        self.pca9685 = pca9685
        self.pca9685.mode1(50)
        
    def setAngle(self, angle):
        self.pca9685.led(self.voie, 0, angle / 360 * 512)
        
    def stop(self):
        self.pca9685.ledOff(self.voie)
