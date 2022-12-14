from pia import PIA
from pcf8574 import PCF8574

class PIA_PCF8574(PIA):
  def __init__(self, pcf8574):
    super().__init__()
    self.pcf8574 = pcf8574
    
  def setOutput(self, value):
#     print("setOutput port : " + str(self.port) + " valeur : " + str(hex(value)))
    self.pcf8574.setOLAT(value)

  def getInput(self):
    value = self.pcf8574.getGPIO()
#     print("getInput port : " + str(self.port) + " valeur : " + str(hex(value)))
    return value
