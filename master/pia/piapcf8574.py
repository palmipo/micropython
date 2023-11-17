from piabus import PiaBus
from pcf8574 import PCF8574

class PiaPcf8574(PiaBus):
  def __init__(self, pcf8574):
    super().__init__()
    self.pcf8574 = pcf8574
    
  def set(self, value):
    self.pcf8574.setOLAT(value)

  def get(self):
    value = self.pcf8574.getGPIO()
    return value
