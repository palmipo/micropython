from pia import PIA
from pcf8574a import PCF8574A

class PIA_PCF8574A(PIA):
  def __init__(self, pia):
    super().__init__()
    self.pia = pia
    
  def setOutput(self, value):
#     print("setOutput port : " + str(self.port) + " valeur : " + str(hex(value)))
    self.pia.setOLAT(value)

  def getInput(self):
    value = self.pia.getGPIO()
#     print("getInput port : " + str(self.port) + " valeur : " + str(hex(value)))
    return value
