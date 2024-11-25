from neopixel import NeoPixel
from device.afficheur.lcd_1inch14 import Lcd_1inch14
from master.pia.piapico import PiaOutputPico
from master.pwm.pwmpico import PwmPico
from master.spi.spipico import SpiPico
from waveshare.waveshare_nixie_clock.nixiespipico import NixieSpiPico
import machine

class NixieLcd:
    def __init__(self, rst_pin, dc_pin, bl_pin, led_pin):
#         self.width = 135
#         self.height = 240

        self.leds = NeoPixel(machine.Pin(led_pin, machine.Pin.OUT), 6) # 22
        for led in self.leds:
            led = (0, 0, 0)
        self.leds.write()

        self.rst = PiaOutputPico(rst_pin) # 12
        self.rst.set(1)

        self.spi = NixieSpiPico(csa1=PiaOutputPico(2), csa2=PiaOutputPico(3), csa3=PiaOutputPico(4), spi=SpiPico(1, sck=machine.Pin(10), mosi=machine.Pin(11), miso=None))

        self.dc = PiaOutputPico(dc_pin) # 8
        self.dc.set(1)

        self.bl = PwmPico(bl_pin) # 13

        self.LCDs = []
        for num in range (0,6):
            self.LCDs.append(Lcd_1inch14(num, self.dc, self.rst, self.spi, self.bl))

    def setLedColor(self, num, r, g, b):
        self.leds[num] = (r, g, b)
        self.leds.write()
       
    def reset_all(self):
        """Reset the display"""
        self.rst.set(0)
        time.sleep(1)
        self.rst.set(1)
        time.sleep(1)
