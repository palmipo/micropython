from neopixel import NeoPixel
from master.pia.piapico import PiaOutputPico
from master.pwm.pwmpico import PwmPico
from device.pwm.servomoteur import ServoMoteur
from device.pia.hc_sr04 import HC_SR04
from tools.configfile import ConfigFile
import time

# servo_pin = 7/8/25 -> broche 26/24/22
# led_pin = 18 -> broche 12
# ultrasonc_trigger_pin = 27 -> broche 13
# ultrasonic_echo_pin = 22 -> broche 15
# motor1 = 24/23 -> broche 18/16
# motor2 = 5/6 -> broche 29/31
# line_tracker = 16/20/21 -> broche 36/38/40

class Freenove:
    class Motor:
        def __init__(self, pin1, pin2):
            self.motor1 = PiaOutputPico(pin1)
            self.motor2 = PiaOutputPico(pin2)
        
        def reverte(self):
            self.motor1.set(1)
            self.motor2.set(0)
        
        def forward(self):
            self.motor1.set(0)
            self.motor2.set(1)
        
        def stop(self):
            self.motor1.set(0)
            self.motor2.set(0)

    class Tank:
        def __init__(self):
            cfg = ConfigFile('/config.json')
            self.led_pin = PiaOutputPico(cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['led']]])
            self.leds = NeoPixel(self.led_pin.pin, 4)
            self.motorL = Freenove.Motor(cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['motorLF']]],
                                         cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['motorLR']]])
            self.motorR = Freenove.Motor(cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['motorRF']]],
                                         cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['motorRR']]])
            self.servo_pin = []
            self.servo_pin.append(ServoMoteur(PwmPico(cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['servo1']]])))
            self.servo_pin.append(ServoMoteur(PwmPico(cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['servo2']]])))
            self.servo_pin.append(ServoMoteur(PwmPico(cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['servo3']]])))
            self.ultrasonic = HC_SR04(cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['ultrasonc_trigger']]],
                                      cfg.config()['motherboard']['rp2040_pizero'][cfg.config()['motherboard']['raspi'][cfg.config()['freenove']['tank']['ultrasonic_echo']]])

        def led(self, num, r, g, b):    
            self.leds[num%4] = (r, g, b) # set the first pixel to white
            self.leds.write()              # write data to all pixels

        def mesure(self):
            return self.ultrasonic.start()

        def bras(self, num):
            if num == 0:
                self.servo_pin[0].setAngle(0)
            else:
                self.servo_pin[0].setAngle(90)

        def pince(self, num):
            if num == 0:
                self.servo_pin[1].setAngle(0)
            else:
                self.servo_pin[1].setAngle(90)

        def forward(self):
            self.motorL.forward()
            self.motorR.forward()

        def stop(self):
            self.motorL.stop()
            self.motorR.stop()

        def close(self):
            self.servo_pin[0].close()
            self.servo_pin[1].close()
            self.motorL.stop()
            self.motorR.stop()
            for i in range(4):
                self.leds[i] = (0, 0, 0)
            self.leds.write()

if __name__ == "__main__":
    tank = Freenove.Tank()
    tank.led(0, 128, 0, 0)
    tank.led(1, 0, 128, 0)
    tank.led(2, 0, 0, 128)
    tank.led(3, 128, 128, 128)
    tank.forward()
    time.sleep(5)
    tank.stop()
    tank.bras(1)
    tank.pince(1)
    time.sleep(1)
    print(tank.mesure())

    tank.close()
