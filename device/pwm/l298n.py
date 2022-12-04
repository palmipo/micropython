import rp2
from machine import Pin, PWM

class L298N:
    def __init__(self, enA, in1, in2):
        self.enA = PWM(Pin(enA))
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.enA.freq(100000)

    def forward(self, vitesse):
        self.in1.on()
        self.in2.off()
        self.enA.duty_u16(vitesse)

    def reverse(self, vitesse):
        self.in1.off()
        self.in2.on()
        self.enA.duty_u16(vitesse)

    def off(self):
        self.in1.off()
        self.in2.off()
        self.enA.duty_u16(0)

    def stop(self):
        self.in1.on()
        self.in2.on()
        self.enA.duty_u16(65535)
