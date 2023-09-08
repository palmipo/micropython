import time
import machine
from bmp280 import BMP280
from lsm303d import LSM303D
import micropython
micropython.alloc_emergency_exception_buf(100)

# 0x49: ADS1015
# 0x29: TCS3472
# 0x1d: LSM303D
# 0x77: BMP280

class EnviroPHat:
    def __init__(self, i2c, led):
        self.busi2c = i2c
        self.led = machine.Pin(led, machine.Pin.OUT)
        self.led.off()
        self.temperature = BMP280(self.busi2c)
        if self.temperature.chipIdRegister():
            self.temperature.reset()
            time.sleep(1)
            self.temperature.configRegister(3, 4)
        self.gyro = LSM303D(self.busi2c)
        print(self.gyro.who_am_i())
        self.gyro.ctrl5(1, 0, 0, 0, 0)
        for i in range(0, 10):
            time.sleep(1)
            print(self.gyro.temp_out())

#     def ads1015(self):
#         self.bmp = ADS1015(self.busi2c)
#     def tcs3472(self):
#         self.bmp = TCS3472(self.busi2c)
#     def lsm303d(self):
#         self.bmp = LSM303D(self.busi2c)
    def bmp280(self):
        self.temperature.ctrlMeasureRegister(2, 5, 3)
        return self.temperature.compensateT()

# import rp2
# import machine
# from picoi2c import PicoI2C
# from muxi2c import MuxI2C
# from pca9548a import PCA9548A
# 
# i2c = PicoI2C(0, 4, 5)
# try:
#     pca9548a = PCA9548A(0, i2c, 3)
#     pca9548a.reset()
#     time.sleep_ms(100)
# 
#     mux3 = MuxI2C(3, pca9548a, i2c)
#     print(mux3.scan())
# 
#     tst = EnviroPHat(mux3, 2)
#     print(tst.bmp280())

#     tst.led.on()
#     time.sleep(1)
#     tst.led.off()
# except Exception as erreur:
#     print(type(erreur))    # the exception instance
#     print(erreur)    # the exception instance
# finally:
#     pca9548a.clear()
