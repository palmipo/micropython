from st7789 import ST7789
from neopixel import NeoPixel
from machine import Pin
from piapico import PiaPicoOutput
from pwmpico import PwmPico
from spipiconixie import SPIPicoNixie
import time

class Lcd_1inch14(ST7789):
    def __init__(self, num, dc, rst, spi, bl, led):
        self.width = 135
        self.height = 240 
        
        self.DC_PIN = dc
        self.RST_PIN = rst
        self.spi = spi
        self.BL_PIN = bl
        self.BL_PIN.setFrequency(10000)
        self.BL_PIN.setDuty(20)
        self.led = led
        self.led[num] = (0, 0, 0)
        self.led.write()
        
        super().__init__(num)

    def setLedColor(self, num, r, g, b):
        self.led[num] = (r, g, b)
        self.led.write()

    def setLcdBlackLight(self, lev):#0-100
        self.BL_PIN.setDuty(lev % 100)

    def write_cmd(self, num, cmd):
        self.DC_PIN.set(0)
        data = bytearray(1)
        data[0] = cmd
        self.spi.send(num, data)
        
    def write_data(self, num, val):
        self.DC_PIN.set(1)
        data = bytearray(1)
        data[0] = val
        self.spi.send(num, data)

    def write_buffer(self, num, buf):
        self.DC_PIN.set(1)
        for i in range(0,len(buf),4096):
            self.spi.send(num, buf[i:i+4096])
       
    def reset_all(self):
        """Reset the display"""
        self.RST_PIN.set(0)
        time.sleep(1)
        self.RST_PIN.set(1)
        time.sleep(1)
            
if __name__=='__main__':
    w = 135
    h = 240
    import sys    
    try:

        rst=PiaPicoOutput(12)
        rst.set(1)
        spi=SPIPicoNixie()
        dc=PiaPicoOutput(8)
        dc.set(1)
        bl=PwmPico(13)
        led=NeoPixel(Pin(22, Pin.OUT), 6)

        import framebuf            
        buffer = bytearray(w * h * 2)

        test = framebuf.FrameBuffer(buffer, w, h, framebuf.RGB565)

        for num in range (0,6):
            LCD = Lcd_1inch14(num, dc, rst, spi, bl, led)

        for num in range (0,6):
            LCD.setLedColor(num, 0x80, 0, 0xff)
            test.fill(0x00ffffff)
            test.text("coucou {}".format(num), 0, 0)
            LCD.show(num, 0, 0, w, h, buffer)

    except KeyboardInterrupt:
        sys.exit()

