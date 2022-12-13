from bmp280 import BMP280

class EnviroPHat:
    def __init__(self, i2c):
        self.busi2c = i2c

#     def ads1015(self):
#         self.bmp = ADS1015(self.busi2c)
#     def tcs3472(self):
#         self.bmp = TCS3472(self.busi2c)
#     def lsm303d(self):
#         self.bmp = LSM303D(self.busi2c)
    def bmp280(self):
        self.bmp = BMP280(self.busi2c)
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
            t = test.bmp.compensateT()
