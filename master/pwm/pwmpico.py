import rp2
from machine import Pin, PWM
from interface.pwmbus import PwmBus


class PwmPico(PwmBus):
    def __init__(self, pin):
        super().__init__()
        self.pwm = machine.PWM(machine.Pin(pin, machine.Pin.OUT))

    def setFrequency(self, freq):
        self.pwm.freq(freq)
        
    def setDuty(self, pourcentage):
        self.pwm.duty_u16((pourcentage % 100) * 65535 // 100)
