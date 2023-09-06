import rp2
from machine import Pin

class SM5166P:
    def __init__(self, pinA0, pinA1, pinA2):
        self.pinA0 = Pin(pinA0, Pin.OUT)
        self.pinA1 = Pin(pinA1, Pin.OUT)
        self.pinA2 = Pin(pinA2, Pin.OUT)
        
    def setChannel(self, cannal):
        self.pinA0.value(cannal & 0x01)
        self.pinA1.value(cannal & 0x02)
        self.pinA2.value(cannal & 0x04)

