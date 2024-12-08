import machine
import time

class HC_SR04:
    def __init__(self, trigger, echo):
        self.trigger = machine.Pin(trigger, machine.Pin.OUT)
        self.trigger.off()
        self.echo = machine.Pin(echo, machine.Pin.IN)#, machine.Pin.PULL_DOWN)
        self.echo.irq(self.cb, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)#, hard=True)
        self.t0 = 0
        self.t1 = 0

    def start(self):
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()
        self.t0 = 0
        self.t1 = 0
        time.sleep(1)
        delta = time.ticks_diff(self.t1, self.t0)
        return delta * 34 // 2000 # vitesse du son dans l'air 340 m/s
        
    def cb(self, pin):
        state = machine.disable_irq()
        if self.t0 == 0:
            self.t0 = time.ticks_us()
        else:
            self.t1 = time.ticks_us()
        machine.enable_irq(state)

# sensor = HC_SR04(27, 22)
# for i in range (0, 100):
#     print(sensor.start())
