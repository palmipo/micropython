from pia import PIA
from mcp23017 import MCP23017

class PIA_MCP23017(PIA):
  def __init__(self, port, pia):
    super().__init__()
    self.port = port
    self.pia = pia
    
  def set(self, value):
    self.pia.set(self.port, value)
   
  def get(self, value):
    self.pia.get(self.port, value)
