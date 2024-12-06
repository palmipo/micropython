from neopixel import NeoPixel
from master.pia.piapico import PiaOutputPico
from master.pwm.pwmpico import PwmPico

class Freenove:
    def __init__(self):
        pass
    
    class Motor:
        def __init__(self, pin1, pin2):
            self.motor1 = PwmPico(pin1)
            self.motor2 = PwmPico(pin2)
#             self.motor1.setFrequency(100000)
#             self.motor2.setFrequency(100000)

        def forward(self):
            self.motor1.setDuty(0)
            self.motor2.setDuty(100)
        
        def reverse(self):
            self.motor1.setDuty(100)
            self.motor2.setDuty(0)

    class Tank:
        def __init__(self):
            self.led_pin = PiaOutputPico(26)   # set GPIO0 to output to drive NeoPixels
            self.leds = NeoPixel(self.led_pin.pin, 4)   # create NeoPixel driver on GPIO0 for 8 pixels
            self.motorL = Freenove.Motor(39, 4)
            self.motorR = Freenove.Motor(34, 35)
            self.servo_pin = []
            self.servo_pin.append(PwmPico(22))
            self.servo_pin.append(PwmPico(5))
            self.servo_pin.append(PwmPico(0))
            for i in range(len(self.servo_pin)):
                self.servo_pin[i].setFrequency(50)
                self.servo_pin[i].setDuty(50)

        def led(self, num, r, g, b):    
            for i in range(4):
                self.leds[num%4] = (r, g, b) # set the first pixel to white
            self.leds.write()              # write data to all pixels

        def servo(self, num, val):
            self.servo_pin[num%3].setDuty(val)

        def motor(self, rigth, left):
            self.motorL.forward()
            self.motorR.forward()
        

tank = Freenove.Tank()
tank.led(0, 128, 0, 0)
tank.servo(0, 50)
