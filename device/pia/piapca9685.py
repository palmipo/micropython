from interface.piabus import PiaBus
from device.i2c.pca9685 import PCA9685

class PiaPca9685(PiaBus):
  def __init__(self, voie, pca9685):
    super().__init__()
    self.voie = voie
    self.pca9685 = pca9685
    
  def set(self, value):
    if value == True:
        self.pca9685.ledOn(self.voie)
    else:
        self.pca9685.ledOff(self.voie)
