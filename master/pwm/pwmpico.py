import rp2
from machine import Pin, PWM
from pwmbus import PwmBus

class PwmPico(PwmBus):
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))

    def setFrequency(self, freq):
        self.periode = 1/freq
        self.pwm.periode(self.periode)
        
    def setDuty(self, pourcentage):
        self.pwm.duty_ns(pourcentage * self.periode / 100)
