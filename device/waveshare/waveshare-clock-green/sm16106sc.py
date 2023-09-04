import rp2
from machine import Pin

class SM16106SC:
    def __init__(self, pinSDI, pinLE, pinCLK, pinOE_):
        self.pinSDI = Pin(pinSDI, Pin.out)
        self.pinLE = Pin(pinLE, Pin.out)
        self.pinCLK = Pin(pinCLK, Pin.out)
        self.pinOE_ = Pin(pinOE_, Pin.out)

        self.pinSDI.off()
        self.pinCLK.off()
        self.pinLE.off()
        self.pinOE_.on()

    def send(self, data):
        self.pinOE_.on()
        self.pinLE.off()
        self.pinCLK.off()

        for b in data:
            for i in range(8):  
                self.pinCLK.off()
                self.pinSDI.value(b & 0x01)
                self.pinCLK.on()
                b = b >> 1
                timer.sleep_us(1)

        self.pinCLK.off()

    def latch(self):
        self.pinLE.on()
        timer.sleep_us(1)
        self.pinLE.off()

    def OutputEnabled(self):
        self.pinOE_.off()
        timer.sleep_us(1)
        self.pinOE_.on()
