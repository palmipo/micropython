import rp2
from machine import Pin
from busi2c import BusI2C
from mcp23017 import MCP23017
from pia_mcp23017 import PIA_MCP23017
from ada772 import ADA772
from hd44780 import HD44780

i2c = BusI2C(0, Pin(4), Pin(5))

gpio = MCP23017(0, i2c)
gpio.setIODirectionRegister(0, 0x3f)
gpio.setIODirectionRegister(1, 0)

pia1 = PIA_MCP23017(1, gpio)
pia12 = PIA_MCP23017(0, gpio)

lcd_io = ADA772(pia1, pia2)
lcd_io.setBacklight(1)

lcd = HD44780(lcd_io)

