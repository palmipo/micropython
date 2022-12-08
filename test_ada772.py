import rp2
from machine import Pin
from busi2c import BusI2C
from pca9548a import PCA9548A
from ada772 import ADA772
from hd44780 import HD44780


def callback(ADA772):
    print("callback")

i2c = BusI2C(0, Pin(4), Pin(5))

mux = PCA9548A(0, i2c)
mux.setCanal((1<<7)|(1<<6))
circuits = i2c.scan()
print("circuits presents sur le bus i2c : ")
print(circuits)
print()

lcd_io = ADA772(0, i2c, 2, callback)
lcd_io.setBackLight(1)

lcd = HD44780(lcd_io)
lcd.clear()
lcd.home()
lcd.writeText("Hello World !")
while True:
    #lcd_io.scrute()
    True
