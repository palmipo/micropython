import rp2
import machine

class SM5166P:
    def __init__(self, pinA0, pinA1, pinA2):
        self.pinA0 = machine.Pin(pinA0, machine.Pin.OUT)
        self.pinA1 = machine.Pin(pinA1, machine.Pin.OUT)
        self.pinA2 = machine.Pin(pinA2, machine.Pin.OUT)
        
    def setChannel(self, cannal):
        self.pinA0.value(cannal & 0x01)
        self.pinA1.value(cannal & 0x02)
        self.pinA2.value(cannal & 0x04)

