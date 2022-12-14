import rp2
import machine
import time

class HC_SR04:
    def __init__(self, trigger, echo):
        self.trigger = Pin(trigger, Pin.OUT)
        self.trigger.off()
        self.echo = Pin(echo, Pin.IN, Pin.PULL_UP)
        self.echo.irq(self.cb, Pin.IRQ_FALLING | Pin.IRQ_RISING)

    def start(self):
        self.trigger.on()
        time.sleep_ms(10)
        self.trigger.off()
        self.t0 = 0
        self.t1 = 0
        
    def cb(self, pin):
        state = machine.disable_irq()
        if self.t0 == 0:
            self.t0 = time.ticks_us()
        else:
            self.t1 = time.ticks_us()
        machine.enable_irq(state)

    def mesure(self):
        delta = time.ticks_diff(self.t1, self.t0) >> 1
        return self.delta * 340 / 1000 # vitesse du son dans l'air 340 m/s
