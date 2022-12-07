import rp2
from machine import Pin
from busi2c import BusI2C
from pca9548a import PCA9548A
from mcp23017 import MCP23017
from pia_mcp23017 import PIA_MCP23017
from ada772 import ADA772
from hd44780 import HD44780

i2c = BusI2C(0, Pin(4), Pin(5))

mux = PCA9548A(0, i2c)
mux.setCanal((1<<7)|(1<<6))
circuits = i2c.scan()
print("circuits presents sur le bus i2c : ")
print(circuits)
print()

gpio = MCP23017(0, i2c)
gpio.setIODIR(0, 0x1f)
gpio.setGPPU(0, 0x1f)
gpio.setIPOL(0, 0x1f)
gpio.setIODIR(1, 0)

pia1 = PIA_MCP23017(1, gpio)
pia2 = PIA_MCP23017(0, gpio)

lcd_io = ADA772(pia1, pia2)
lcd_io.setBackLight(1)

lcd = HD44780(lcd_io)
lcd.clear()
lcd.home()
lcd.writeText("Hello World !")
while True:
    lcd_io.scrute()