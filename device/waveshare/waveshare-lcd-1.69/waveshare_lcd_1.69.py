from lcd_1inch69 import Lcd_1inch69
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
        
        self.lcd = Lcd_1inch69(dc=Pin(DC,Pin.OUT), cs = Pin(CS,Pin.OUT), rst = Pin(RST,Pin.OUT), br=PWM(Pin(BL)), spi = SPI(0, baudrate=100_000_000, polarity=0, phase=0, sck=Pin(SCK),mosi=Pin(MOSI), miso=None))

        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        self.BLACK =   0x0000
 
    def write_text(self,text,x,y,size,color):
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
    try:
        width = 240
        height = 280
        LCD = WaveShare_Lcd_1inch69(width, height)
        #color BRG
        LCD.fill(LCD.WHITE)
        LCD.lcd.show(0, 0, 240, 280, LCD.buffer)
        
        LCD.fill_rect(0,0,width,30,LCD.RED)
        LCD.write_text("Raspberry Pico",10,8,2,LCD.WHITE)
        
        LCD.fill_rect(0,30,width,30,LCD.BLUE)
        LCD.rect(0,30,width,30,LCD.BLACK)
        LCD.write_text("Pico-LCD-1.69",10,38,2,LCD.WHITE)
        
        LCD.fill_rect(0,60,width,30,LCD.GREEN)
        LCD.rect(0,60,width,30,LCD.BLACK)
        LCD.write_text("Crapaud",10,68,2,LCD.WHITE)
        
        now = time.localtime()
        LCD.fill_rect(0,90,width,30,0X07FF)
        LCD.rect(0,90,width,30,LCD.BLACK)
        LCD.write_text("Time: {}:{}".format(now[3], now[4]),10,98,2,LCD.WHITE)

        LCD.fill_rect(0,120,width,30,0xF81F)
        LCD.fill_rect(0,150,width,30,0xFFE0)
        
        LCD.lcd.show(0, 0, 240, 280, LCD.buffer)
    except KeyboardInterrupt:
        sys.exit()
