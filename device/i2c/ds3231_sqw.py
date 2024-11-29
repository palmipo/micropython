from device.i2c.ds3231 import DS3231
from master.pia.piaisrpico import PiaIsrPico

class DS3231_SQW(DS3231):
    def __init__(self, address, bus, pinSQW):
        super().__init__(address, bus)

        self.pinSQW = PiaIsrPico(pinSQW)

    def isActivated(self):
        return self.pinSQW.isActivated()

    def isAlarm1Activated(self):
        OSF, EN32kHz, BSY, A2F, A1F = self.getStatusRegister()
        return A1F == 0x01

    def isAlarm2Activated(self):
        OSF, EN32kHz, BSY, A2F, A1F = self.getStatusRegister()
        return A2F == 0x01
# 
# try:
#     from master.i2c.i2cpico import I2CPico
#     from device.i2c.ds3231_sqw import DS3231_SQW
#     import time
#     i2c = I2CPico(1, 6, 7)
#     ds1321 = DS3231_SQW(0, i2c, 18)
#     ds1321.setAlarm1(A1M=0x0F, hour='08:00:00', day='03')
#     ds1321.setControlRegister(CONV=0x01, RS=0x00, INTCN=0x00, A2IE=0x00, A1IE=0x01, EN32kHz=0)
#     fin = False
#     while fin == False:
#         if ds1321.isActivated() == True:
#             print('rtc')
# 
#         time.sleep_ms(500)
# except KeyboardInterrupt:
#     pass
# 
# finally:
#     fin = True
#     ds1321.setControlRegister(0, 0, 0, 0, 0)
