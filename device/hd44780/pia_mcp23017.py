from pia import PIA
from mcp23017 import MCP23017

class PIA_MCP23017(PIA):
  def __init__(self, port, pia):
    super().__init__()
    self.port = port
    self.pia = pia
    
  def setOutput(self, value):
    self.pia.setOLAT(self.port, value)
   
  def getInput(self):
    return self.pia.getGPIO(self.port)
