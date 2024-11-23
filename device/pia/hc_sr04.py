import machine
import time

class HC_SR04:
    def __init__(self, trigger, echo):
        self.trigger = machine.Pin(trigger, machine.Pin.OUT)
        self.trigger.off()
        self.echo = machine.Pin(echo, machine.Pin.IN)
        self.echo.irq(self.cb, machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)#, hard=True)
        self.t0 = 0
        self.t1 = 0

    def start(self):
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()
        self.t0 = 0
        self.t1 = 0
        time.sleep_ms(60)
        delta = time.ticks_diff(self.t1, self.t0)
        return delta * 17165 / 1000 # vitesse du son dans l'air 340 m/s
        
    def cb(self, pin):
        state = machine.disable_irq()
        if self.t0 == 0:
            self.t0 = time.ticks_cpu()
        else:
            self.t1 = time.ticks_cpu()
        machine.enable_irq(state)

sensor = HC_SR04(15, 14)
for i in range (0, 100):
    print(sensor.start())
    time.sleep(1)
