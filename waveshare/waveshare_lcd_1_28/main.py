from machine import Pin,I2C,SPI,PWM,ADC
import framebuf
import time


DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12

BL = 25

Vbat_Pin = 29

if __name__=='__main__':

    rst = Pin(RST,Pin.OUT)
    rst(1)
    cs = Pin(CS,Pin.OUT)
    cs(1)
    spi = SPI(1,100_000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
    dc = Pin(DC,Pin.OUT)
    dc(1)
    pwm = PWM(Pin(BL))

    from lcd_1inch28 import LCD_1inch28
    LCD = LCD_1inch28(dc, rst, cs, spi, pwm)
    LCD.set_bl_pwm(0xFFFF)


    buffer = bytearray(LCD.height * LCD.width * 2)
    painter = framebuf.FrameBuffer(buffer, LCD.width, LCD.height, framebuf.RGB565)

    
    red   =   0x07E0
    green =   0x001f
    blue  =   0xf800
    white =   0xffff
    
    painter.fill(white)
    LCD.show(buffer)

    from qmi8658 import QMI8658
    I2C_SDA = 6
    I2C_SDL = 7
    qmi8658 = QMI8658(I2C(id=1,scl=Pin(I2C_SDL),sda=Pin(I2C_SDA),freq=100_000))
    Vbat= ADC(Pin(Vbat_Pin))   
    
    while(True):
        xyz=qmi8658.Read_XYZ()
        
        painter.fill(white)
        
        painter.fill_rect(0,0,240,40,red)
        painter.text("RP2040-LCD-1.28",60,25,white)
        
        painter.fill_rect(0,40,240,40,blue)
        painter.text("Waveshare",80,57,white)
        
        painter.fill_rect(0,80,120,120,0x1805)
        painter.text("ACC_X={:+.2f}".format(xyz[0]),20,100-3,white)
        painter.text("ACC_Y={:+.2f}".format(xyz[1]),20,140-3,white)
        painter.text("ACC_Z={:+.2f}".format(xyz[2]),20,180-3,white)

        painter.fill_rect(120,80,120,120,0xF073)
        painter.text("GYR_X={:+3.2f}".format(xyz[3]),125,100-3,white)
        painter.text("GYR_Y={:+3.2f}".format(xyz[4]),125,140-3,white)
        painter.text("GYR_Z={:+3.2f}".format(xyz[5]),125,180-3,white)
        
        painter.fill_rect(0,200,240,40,0x180f)
        reading = Vbat.read_u16()*3.3/65535*2
        painter.text("Vbat={:.2f}".format(reading),80,215,white)
        
        LCD.show(buffer)
        time.sleep(0.1)
