from devicei2c import DeviceI2C
from machine import Pin
import time
class PCA9548A(DeviceI2C):

    def __init__(self, address, bus, reset_pin=0):
        super().__init__(0x70 | (address & 0x03), bus)
        self.reset_ = Pin(reset_pin, Pin.OUT)
        self.reset_.on()

    def reset(self):
        self.reset_.off()
        time.sleep_ms(1)
        self.reset_.on()

    def clear(self):
        cmd = bytearray(1)
        cmd[0] = 0
        self.busi2c.send(self.adresse, cmd)

    def setCanal(self, canal):
        cmd = bytearray(1)
        cmd[0] = canal & 0xff
        self.busi2c.send(self.adresse, cmd)
