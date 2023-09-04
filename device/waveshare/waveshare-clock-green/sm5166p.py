import rp2
from machine import Pin

class SM5166P:
    def __init__(self, pinA0, pinA1, pinA2):
        self.pinA0 = Pin(pinA0, Pin.out)
        self.pinA1 = Pin(pinA1, Pin.out)
        self.pinA2 = Pin(pinA2, Pin.out)
        
    def setChannel(self, cannal):
        self.pinA0.value(canal & 0x01)
        self.pinA1.value(canal & 0x02)
        self.pinA2.value(canal & 0x04)

