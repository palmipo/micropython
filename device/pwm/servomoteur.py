class ServoMoteur:
    def __init__(self, pwm):
        self.pwm = pwm
        self.pwm.setFrequency(50) # periode 20ms
        
        # angle de 0 => 1ms
        # angle de 90° => 1.5ms
        # angle de 180° => 2ms
    def setAngle(self, angle):
        ms = 65536//20
        print('ms = {}, angle = {} => {}'.format(ms, angle, (angle % 180) * 2 // 180))
        self.pwm.setDuty(ms + (angle % 180) * ms // 180)
    
    def close(self):
        self.pwm.setDuty(0)
