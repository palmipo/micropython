import rp2
from machine import Pin, PWM

class BusPwm:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))

    def setFrequency(self, freq):
        pwm.periode(1/freq)
        
    def setDuty(self, pourcentage):
        pwm.duty_ns(pourcentage * self.periode / 100)
