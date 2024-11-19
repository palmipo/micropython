import machine

class L298N:
    def __init__(self, enA, in1, in2, freq=100000):
        self.enA = machine.PWM(machine.Pin(enA))
        self.in1 = machine.Pin(in1, machine.Pin.OUT)
        self.in2 = machine.Pin(in2, machine.Pin.OUT)
        self.enA.freq(freq)

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
