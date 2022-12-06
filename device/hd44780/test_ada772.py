from busi2c import BusI2C
from mcp23017 import MCP23017
from pia_mcp23017 import PIA_MCP23017
from ada772 import ADA772
from hd44780 import HD44780

i2c = BusI2C(0, 4, 5, 100000)
gpio = MCP23017(i2c)
pia = PIA_ADA772(1, gpio)
lcd_io = ADA772(pia)
lcd = HD44780(lcd_io)

lcd_io.setBacklight(1)
