
from machine import Pin,SPI,PWM
import framebuf
import time
import os

BL = 22
DC = 20
RST = 21
MOSI = 19
SCK = 18
CS = 17


class WaveShare_Lcd_1inch69(framebuf.FrameBuffer):
    def __init__(self, w, h):
        self.width = 240
        self.height = 280
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(0)
        self.spi = SPI(0,1000_000)
        self.spi = SPI(0,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        self.BLACK =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x00)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0B)
        self.write_data(0x0B)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x35)

        self.write_cmd(0xB7)
        self.write_data(0x11) 

        self.write_cmd(0xBB)
        self.write_data(0x35)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x0D)   

        self.write_cmd(0xC4)
        self.write_data(0x20) # VDV, 0x20: 0V

        self.write_cmd(0xC6)
        self.write_data(0x13) # 0x13: 60Hz 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xD6)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xF0)
        self.write_data(0x06)
        self.write_data(0x0B)
        self.write_data(0x0A)
        self.write_data(0x09)
        self.write_data(0x26)
        self.write_data(0x29)
        self.write_data(0x33)
        self.write_data(0x41)
        self.write_data(0x18)
        self.write_data(0x16)
        self.write_data(0x15)
        self.write_data(0x29)
        self.write_data(0x2D)

        self.write_cmd(0xE1)
        self.write_data(0xF0)
        self.write_data(0x04)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x07)
        self.write_data(0x03)
        self.write_data(0x28)
        self.write_data(0x32)
        self.write_data(0x40)
        self.write_data(0x3B)
        self.write_data(0x19)
        self.write_data(0x18)
        self.write_data(0x2A)
        self.write_data(0x2E)
        
        self.write_cmd(0xE4)
        self.write_data(0x25)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x21)

        self.write_cmd(0x11)

        time.sleep(0.1)

        self.write_cmd(0x29)

    def show(self, x, y, width, height, buffer):
        self.write_cmd(0x36)
        self.write_data(0x00)

        self.write_cmd(0x2A)
        self.write_data(x >> 8)        #Set the horizontal starting point to the high octet
        self.write_data(x & 0xff)    #Set the horizontal starting point to the low octet
        self.write_data((width-1)>>8)        #Set the horizontal end to the high octet
        self.write_data((width-1) & 0xff)  #Set the horizontal end to the low octet 

        self.write_cmd(0x2B)
        self.write_data((y+20) >> 8)
        self.write_data((y+20) & 0xff)
        self.write_data((height+20-1) >> 8)
        self.write_data((height+20-1) & 0xff)
        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buffer)
        self.cs(1)

    def write_text(self,text,x,y,size,color):
        ''' Method to write Text on OLED/LCD Displays
            with a variable font size
            Args:
                text: the string of chars to be displayed
                x: x co-ordinate of starting position
                y: y co-ordinate of starting position
                size: font size of text
                color: color of text to be displayed
        '''
        background = self.pixel(x,y)
        info = []
        # Creating reference charaters to read their values
        self.text(text,x,y,color)
        for i in range(x,x+(8*len(text))):
            for j in range(y,y+8):
                # Fetching amd saving details of pixels, such as
                # x co-ordinate, y co-ordinate, and color of the pixel
                px_color = self.pixel(i,j)
                info.append((i,j,px_color)) if px_color == color else None
        # Clearing the reference characters from the screen
        self.text(text,x,y,background)
        # Writing the custom-sized font characters on screen
        for px_info in info:
            self.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2])   
  
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    width = 240
    height = 280
    LCD = WaveShare_Lcd_1inch69(width, height)
    #color BRG
    LCD.fill(LCD.WHITE)
    LCD.show(0, 0, 240, 280, LCD.buffer)
    
    LCD.fill_rect(0,0,width,30,LCD.RED)
    LCD.write_text("Raspberry Pi Pico",10,8,2,LCD.WHITE)
    
    LCD.fill_rect(0,30,width,30,LCD.BLUE)
    LCD.rect(0,30,width,30,LCD.BLACK)
    LCD.write_text("Pico-LCD-1.69",10,38,2,LCD.WHITE)
    
    LCD.fill_rect(0,60,width,30,LCD.GREEN)
    LCD.rect(0,60,width,30,LCD.BLACK)
    LCD.write_text("PicoGo",10,68,2,LCD.WHITE)
    
    LCD.fill_rect(0,90,width,30,0X07FF)
    LCD.fill_rect(0,120,width,30,0xF81F)
    LCD.fill_rect(0,150,width,30,0xFFE0)
    
    LCD.show(0, 0, 240, 280, LCD.buffer)




