import time
import machine
from bmp280 import BMP280

import rp2
import machine
from picoi2c import PicoI2C
from muxi2c import MuxI2C
from pca9548a import PCA9548A
import micropython
micropython.alloc_emergency_exception_buf(100)

class EnviroPHat:
    def __init__(self, i2c, led):
        self.busi2c = i2c
        self.led = machine.Pin(led, machine.Pin.OUT)
        self.led.off()
        self.bmp = BMP280(self.busi2c)

#     def ads1015(self):
#         self.bmp = ADS1015(self.busi2c)
#     def tcs3472(self):
#         self.bmp = TCS3472(self.busi2c)
#     def lsm303d(self):
#         self.bmp = LSM303D(self.busi2c)
    def bmp280(self):
        if self.bmp.chipIdRegister():
            self.bmp.reset()
            time.sleep(1)
            self.bmp.configRegister(4, 4)
            self.bmp.readCompensationRegister()
            self.bmp.ctrlMeasureRegister(5, 5, 3)
            mesuring, im_update = self.bmp.statusRegister()
            while mesuring != 0:
                mesuring, im_update = self.bmp.statusRegister()
            self.bmp.rawMeasureRegister()
            t = self.bmp.compensateT()
            return t

# try:
#     i2c = PicoI2C(0, 4, 5)
# 
#     pca9548a = PCA9548A(0, i2c, 3)
#     pca9548a.reset()
#     time.sleep_ms(100)
# 
#     mux3 = MuxI2C(3, pca9548a, i2c)
#     print(mux3.scan())
# 
#     tst = EnviroPHat(mux3, 2)
# 
#     print(tst.bmp280())
# 
#     tst.led.on()
#     time.sleep(1)
#     tst.led.off()
# except:
#     print("exception dans main !")
# finally:
#     test.pca9548a.clear()
#     test.busi2c.deinit()
