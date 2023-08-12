from buspia import BusPia
from mcp23017 import MCP23017

class PIA_MCP23017(BusPia):
  def __init__(self, port, pia):
    super().__init__()
    self.port = port
    self.pia = pia
    
  def setOutput(self, value):
#     print("setOutput port : " + str(self.port) + " valeur : " + str(hex(value)))
    self.pia.setOLAT(self.port, value)
   
  def getInput(self):
    value = self.pia.getGPIO(self.port)
#     print("getInput port : " + str(self.port) + " valeur : " + str(hex(value)))
    return value
