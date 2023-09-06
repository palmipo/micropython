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
        n_ack = self.busi2c.writeto(addr, cmd)
        if (len(cmd) != n_ack):
            print(n_ack)
    
    def recv(self, addr, n_byte):
        return self.busi2c.readfrom(addr, n_byte)
    
    def transferer(self, addr, cmd, n_byte):
        self.busi2c.writeto(addr, cmd, False)
        return self.busi2c.readfrom(addr, n_byte)
