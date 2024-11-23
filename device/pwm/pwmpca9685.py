from interface.pwmbus import PwmBus
from device.i2c.pca9685 import Pca9685

class PwmPca9685(PwmBus):
    def __init__(self, num, pca9685):
        super()).__init__()
        self.voie = voie
        self.pca9685 = pca9685

    def setFrequency(self, freq):
        self.pca9685.mode1(freq)
        
    def setDuty(self, pourcentage):
        self.pca9685.led(self.voie, pourcentage * 4096 // 100, 0)

