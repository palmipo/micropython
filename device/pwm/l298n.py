class L298N:
    def __init__(self, enA, in1, in2, freq):
        self.in1 = in1
        self.in2 = in2
        self.enA = enA
        self.enA.setFrequency(freq)

    def forward(self, vitesse):
        self.in1.set(1)
        self.in2.set(0)
        self.enA.setDuty(vitesse)

    def reverse(self, vitesse):
        self.in1.set(0)
        self.in2.set(1)
        self.enA.setDuty(vitesse)

    def off(self):
        self.in1.set(0)
        self.in2.set(0)
        self.enA.setDuty(0)

    def stop(self):
        self.in1.set(1)
        self.in2.set(1)
        self.enA.setDuty(100)
