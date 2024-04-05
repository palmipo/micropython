import rp2
from machine import Pin, I2C
from i2cbus import I2CBus

class I2CPico(I2CBus):
    def __init__(self, n_bus, sda_pin, scl_pin):
      super().__init__()
      self.busi2c = I2C(id=n_bus, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=100000)

    def scan(self):
        return self.busi2c.scan()
        
    def send(self, addr, cmd):
#         try:
            self.busi2c.writeto(addr, cmd)
#         except OSError:
#             print("erreur send i2c")
    
    def recv(self, addr, n_byte):
#         try:
            return self.busi2c.readfrom(addr, n_byte)
#         except OSError:
#             print("erreur recv i2c")

    def transferer(self, addr, cmd, n_byte):
#         try:
            self.busi2c.writeto(addr, cmd, False)
            return self.busi2c.readfrom(addr, n_byte)
#         except OSError:
#             print("erreur transferer i2c")
