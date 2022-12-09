import rp2
from machine import Pin
from picoi2c import PicoI2C
from pca9548a import PCA9548A
# from is31fl3731 import IS31FL3731
# from bmp280 import BMP280
from ds1307 import DS1307
# from ds1621 import DS1621
# from mcp23017 import MCP23017
# from l298n import L298N
from lcd2004 import LCD2004
from hd44780 import HD44780
import time

i2c = PicoI2C(0, Pin(4), Pin(5))
circuits = i2c.scan()
print("liste des circuits i2c presents sur le bus :")
print(circuits)

if (len(circuits) != 0):
    mux = PCA9548A(0, i2c)
    mux.reset()
    
    mux.setCanal((1<<2) | (1<<7)) # 2 : (0x27)lcd2004 # 7 : (0x50)memeoire / (0x68)rtc
    circuits = i2c.scan()
    print("liste des circuits i2c presents sur le bus multiplexe :")
    print(circuits)
    
    lcd_io = LCD2004(0, i2c)
    lcd_io.setBackLight(1)
    lcd = HD44780(lcd_io)
    lcd.home()
    lcd.clear()
    lcd.writeText("Hello World !")
#     bmp = BMP280(i2c)
#     if bmp.chipIdRegister():
#         bmp.reset()
#         time.sleep(1)
#         bmp.ctrlMeasureRegister(5, 5, 3)
#         bmp.configRegister(4, 4)
#         bmp.readCompensationRegister()
#         bmp.ctrlMeasureRegister(5, 5, 3)
#         print(bmp.rawMeasureRegister())
#         print(bmp.compensateT())
#         time.sleep(1)
#         print(bmp.rawMeasureRegister())
#         print(bmp.compensateT())
#         time.sleep(1)
#         print(bmp.rawMeasureRegister())
#         print(bmp.compensateT())
#         time.sleep(1)
#         print(bmp.rawMeasureRegister())
#         print(bmp.compensateT())

#     pia = MCP23017(0, i2c)

#     matrix = IS31FL3731(0, i2c)
#     matrix.shutdown(1)
#     time.sleep(1)
# 
#     matrix.configurationRegister(0, 0)
#     matrix.pictureDisplayRegister(0)
#     matrix.displayOptionRegister(0, 1, 1)
#     matrix.autoplayControlRegister(0, 0, 0)
#     matrix.breathControlRegister(0, 0, 0, 0)
# 
#     led = bytearray(18)
#     blink = bytearray(18)
#     pwm = bytearray(144)
# 
#     for i in range(0, 18):
#         led[i] = 0
#         blink[i] = 0
# 
#     for i in range(0, 144):
#         pwm[i]=0xf
#     
#     for i in range(0, 8):
#         matrix.frameRegister(i, led, blink, pwm)
# 
#     while True:
#         for i in range(0, 18):
#             led[i] = 0xff
#             matrix.frameRegister(0, led, blink, pwm)
#             time.sleep_ms(10)
#         for i in range(0, 18):
#             led[17-i] = 0
#             matrix.frameRegister(0, led, blink, pwm)
#             time.sleep_ms(10)
#     matrix.shutdown(0)

#     t = DS1621(0, i2c)
#     t.start()
#     for i in range(0, 10):
#         print(t.readTemperature())
#     t.stop()
        
    rtc = DS1307(0, i2c)
    rtc.setDate("02/11/22")
    rtc.setTime("06:44:30")
#     rtc.setSquareWave(1)
#     rtc.setMemory(0, 12)
#     rtc.setDayWeek(3)
#     rtc.setOut(0)
#     print(rtc.getMemory(0))
    print(rtc.getDayWeek(), rtc.getDate(), rtc.getTime())

    while True:
        lcd.home()
        lcd.writeText(str(" " + rtc.getDate() + " " + rtc.getTime()))
        time.sleep(1)
        
#     pontH1 = L298N(15, 10, 11)
#     pontH1.forward(65535)
# 
#     pontH2 = L298N(16, 13, 12)
#     pontH2.forward(65535)
#     
#     time.sleep(5)
# 
#     pontH1.off()
#     pontH2.off()

    mux.clear()