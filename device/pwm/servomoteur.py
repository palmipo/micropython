class ServoMoteur:
    def __init__(self, pwm):
        self.pwm = pwm
        self.pwm.setFrequency(50) # periode 20ms
        
        # angle de 0 => 1ms
        # angle de 90° => 1.5ms
        # angle de 180° => 2ms
    def setAngle(self, angle):
        ms = 65536//20
        print('ms = {}, angle = {} => {}'.format(ms, angle, (angle % 360) * 2 // 360))
        self.pwm.setDuty(ms + (angle % 360) * ms // 180)
        
import time
from master.pwm.pwmpico import PwmPico
p = PwmPico(0)
print (p.pwm)
s = ServoMoteur(p)
s.setAngle(0)
for i in range(0, 180):
    s.setAngle(i)
    time.sleep_ms(100)
