from interface.piabus import PiaBus
from device.i2c.mcp23017 import MCP23017

class PiaMCP23017(PiaBus):
  def __init__(self, port, pia):
    super().__init__()
    self.port = port
    self.pia = pia
    
  def set(self, value):
    self.pia.setOLAT(self.port, value)
   
  def get(self):
    value = self.pia.getGPIO(self.port)
    return value
