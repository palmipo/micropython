import rp2
import time
import machine

class SM16106SC:
    TEMPO = 1
    def __init__(self, pinCLK, pinSDI, pinLE, pinOE_):
        self.pinSDI = machine.Pin(pinSDI, machine.Pin.OUT)
        self.pinLE = machine.Pin(pinLE, machine.Pin.OUT)
        self.pinCLK = machine.Pin(pinCLK, machine.Pin.OUT)
        self.pinOE_ = machine.Pin(pinOE_, machine.Pin.OUT)

        self.pinSDI.off()
        self.pinCLK.off()
        self.pinLE.off()
        self.pinOE_.on()

    def send(self, data):
        self.pinCLK.value(0)

        for b in data:
            for i in range(8):  
                self.pinCLK.value(0)
                time.sleep_us(self.TEMPO)
                
                self.pinSDI.value(b & 0x01)
                self.pinCLK.value(1)
                time.sleep_us(self.TEMPO)

                b = b >> 1

        self.pinCLK.value(0)

    def latch(self):
        self.pinLE.on()
        time.sleep_us(self.TEMPO)
        self.pinLE.off()

    def OutputEnable(self):
        self.pinOE_.off()

    def OutputDisable(self):
        self.pinOE_.on()
