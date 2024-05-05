from st7789v import ST7789V
import time, framebuf

class LcdNixie(ST7789V):
    def __init__(self, lcd_num, rst, dc, spi, backlight, led):
        self.width = 135
        self.height = 240 
        
        self.DC_PIN = dc
        self.DC_PIN.set(1)
        self.BL_PIN = backlight
        self.BL_PIN.setFrequency(100)
        self.RST_PIN = rst
        self.RST_PIN.set(1)
        self.lcd_num = lcd_num
        self.led = led
        self.spi = spi
        
        super().__init__()

    def setLedColor(self, r, g, b):
        self.led[self.lcd_num] = (r, g, b)
        self.led.write()

    def setLcdBlackLight(self, lev):#0-10
        self.BL_PIN.setDuty(lev)
        
    def show(self, Xstart, Ystart, Xend, Yend, buffer):
        x = 52
        y = 40
#         self.write_cmd(0x36)
#         self.write_data(0x00)

        self.write_cmd(0x2A)
        self.write_data((Xstart + x) >> 8)        #Set the horizontal starting point to the high octet
        self.write_data((Xstart + x) & 0xff)    #Set the horizontal starting point to the low octet
        self.write_data((Xend - 1 + x)>>8)        #Set the horizontal end to the high octet
        self.write_data((Xend - 1 + x) & 0xff)  #Set the horizontal end to the low octet 

        self.write_cmd(0x2B)
        self.write_data((Ystart + y) >> 8)
        self.write_data((Ystart + y) & 0xff)
        self.write_data((Yend + y - 1) >> 8)
        self.write_data((Yend + y - 1) & 0xff)

        self.write_cmd(0x2C)
        self.DC_PIN.set(1)
        for i in range(0, len(buffer), 4096):
            self.spi.send(self.lcd_num, buffer[i:i+4096])

    def write_cmd(self, cmd):
        self.DC_PIN.set(0)
        data = bytearray(1)
        data[0] = cmd & 0xFF
        self.spi.send(self.lcd_num, data)
        
    def write_data(self, val):
        self.DC_PIN.set(1)
        data = bytearray(1)
        data[0] = val & 0xFF
        self.spi.send(self.lcd_num, data)

    def reset(self):
        """Reset the display"""
        self.RST_PIN.set(1)
        time.sleep_ms(100)
        
        self.RST_PIN.set(0)
        time.sleep_ms(100)
        
        self.RST_PIN.set(1)
        time.sleep_ms(100)
            
            
if __name__=='__main__':
    print("LCD test")
    
    from pwmpico import PwmPico
    from piapico import PiaPicoOutput
    from spipiconixie import SPIPicoNixie
    from neopixel import NeoPixel
    from machine import Pin


    LCD = LcdNixie(1, rst=PiaPicoOutput(12), dc=PiaPicoOutput(7), spi=SPIPicoNixie(), backlight=PwmPico(13), led=NeoPixel(Pin(22, Pin.OUT), 6))
    LCD.setLcdBlackLight(100)
    LCD.setLedColor(128, 0, 255)

    buffer = bytearray(LCD.width * LCD.height * 3)
    frame = framebuf.FrameBuffer(buffer, LCD.width, LCD.height, framebuf.RGB565)
    frame.text('hello world', 0, 0)

    LCD.show(0, 0, LCD.width, LCD.height, buffer)

