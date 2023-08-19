from piabus import PiaBus
from mcp23017 import MCP23017

class PiaMCP23017(PiaBus):
  def __init__(self, port, pia):
    super().__init__()
    self.port = port
    self.pia = pia
    
  def setOutput(self, value):
    self.pia.setOLAT(self.port, value)
   
  def getInput(self):
    value = self.pia.getGPIO(self.port)
    return value
