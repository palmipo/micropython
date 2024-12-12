from neopixel import NeoPixel
from master.pia.piapico import PiaOutputPico
from master.pwm.pwmpico import PwmPico
from device.pwm.servomoteur import ServoMoteur
from device.pia.hc_sr04 import HC_SR04
import time

# servo_pin = 7/8/25
# led_pin = 18
# ultrasonc_trigger_pin = 27
# ultrasonic_echo_pin = 22
# motor1 = 24/23
# motor2 = 5/6
# line_tracker = 16/20/21

class Freenove:
    class Motor:
        def __init__(self, pin1, pin2):
            self.motor1 = PiaOutputPico(pin1)
            self.motor2 = PiaOutputPico(pin2)
        
        def forward(self):
            self.motor1.set(1)
            self.motor2.set(0)
        
        def reverte(self):
            self.motor1.set(0)
            self.motor2.set(1)
        
        def stop(self):
            self.motor1.set(0)
            self.motor2.set(0)

    class Tank:
        def __init__(self):
            self.led_pin = PiaOutputPico(18)
            self.leds = NeoPixel(self.led_pin.pin, 4)
            self.motorL = Freenove.Motor(24, 23)
            self.motorR = Freenove.Motor(15, 6)
            self.servo_pin = []
            self.servo_pin.append(ServoMoteur(PwmPico(7)))
            self.servo_pin.append(ServoMoteur(PwmPico(8)))
            self.servo_pin.append(ServoMoteur(PwmPico(25)))
            self.ultrasonic = HC_SR04(27, 22)

        def led(self, num, r, g, b):    
            for i in range(4):
                self.leds[num%4] = (r, g, b) # set the first pixel to white
            self.leds.write()              # write data to all pixels

        def servo(self, num, val):
            self.servo_pin[num%3].setAngle(val)

        def forward(self):
            self.motorL.forward()
            self.motorR.forward()

        def stop(self):
            self.motorL.stop()
            self.motorR.stop()
        

tank = Freenove.Tank()
tank.led(0, 128, 0, 0)
tank.led(1, 0, 128, 0)
tank.led(2, 0, 0, 128)
tank.forward()
time.sleep(5)
tank.stop()
for i in range(36):
    tank.servo(0, 10*i)
    tank.servo(1, 10*i)
    tank.servo(2, 10*i)
    time.sleep(1)
print(tank.ultrasonic.start())

