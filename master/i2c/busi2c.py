from machine import Pin, I2C
import rp2

class BusI2C:
    def __init__(self, n_bus, sda_pin, scl_pin):
        self.busi2c = I2C(id=n_bus, sda=sda_pin, scl=scl_pin, freq=100000)
    
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