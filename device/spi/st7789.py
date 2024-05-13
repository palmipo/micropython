import time

ST7789_NOP = 0x00
ST7789_SWRESET = 0x01
ST7789_RDDID = 0x04
ST7789_RDDST = 0x09

ST7789_SLPIN = 0x10
ST7789_SLPOUT = 0x11
ST7789_PTLON = 0x12
ST7789_NORON = 0x13

ST7789_INVOFF = 0x20
ST7789_INVON = 0x21
ST7789_DISPOFF = 0x28
ST7789_DISPON = 0x29

ST7789_CASET = 0x2A
ST7789_RASET = 0x2B
ST7789_RAMWR = 0x2C
ST7789_RAMRD = 0x2E

ST7789_PTLAR = 0x30
ST7789_MADCTL = 0x36
ST7789_COLMOD = 0x3A

ST7789_FRMCTR1 = 0xB1
ST7789_FRMCTR2 = 0xB2
ST7789_FRMCTR3 = 0xB3
ST7789_INVCTR = 0xB4
ST7789_DISSET5 = 0xB6

ST7789_GCTRL = 0xB7
ST7789_GTADJ = 0xB8
ST7789_VCOMS = 0xBB

ST7789_LCMCTRL = 0xC0
ST7789_IDSET = 0xC1
ST7789_VDVVRHEN = 0xC2
ST7789_VRHS = 0xC3
ST7789_VDVS = 0xC4
ST7789_VMCTR1 = 0xC5
ST7789_FRCTRL2 = 0xC6
ST7789_CABCCTRL = 0xC7

ST7789_RDID1 = 0xDA
ST7789_RDID2 = 0xDB
ST7789_RDID3 = 0xDC
ST7789_RDID4 = 0xDD

ST7789_GMCTRP1 = 0xE0
ST7789_GMCTRN1 = 0xE1

ST7789_PWCTR6 = 0xFC

class ST7789:
    def __init__(self, num):
        self.write_cmd(num, ST7789_SWRESET)    # Software reset
        time.sleep(0.150)               # delay 150 ms

        self.write_cmd(num, 0x36)
        self.write_data(num, 0x00)

        self.write_cmd(num, 0x3A) 
        self.write_data(num, 0x05)

        self.write_cmd(num, 0xB2)
        self.write_data(num, 0x0C)
        self.write_data(num, 0x0C)
        self.write_data(num, 0x00)
        self.write_data(num, 0x33)
        self.write_data(num, 0x33)

        self.write_cmd(num, 0xB7)
        self.write_data(num, 0x35) 

        self.write_cmd(num, 0xBB)
        self.write_data(num, 0x19)

        self.write_cmd(num, 0xC0)
        self.write_data(num, 0x2C)

        self.write_cmd(num, 0xC2)
        self.write_data(num, 0x01)

        self.write_cmd(num, 0xC3)
        self.write_data(num, 0x12)   

        self.write_cmd(num, 0xC4)
        self.write_data(num, 0x20)

        self.write_cmd(num, 0xC6)
        self.write_data(num, 0x0F) 

        self.write_cmd(num, 0xD0)
        self.write_data(num, 0xA4)
        self.write_data(num, 0xA1)

        self.write_cmd(num, 0xE0)
        self.write_data(num, 0xD0)
        self.write_data(num, 0x04)
        self.write_data(num, 0x0D)
        self.write_data(num, 0x11)
        self.write_data(num, 0x13)
        self.write_data(num, 0x2B)
        self.write_data(num, 0x3F)
        self.write_data(num, 0x54)
        self.write_data(num, 0x4C)
        self.write_data(num, 0x18)
        self.write_data(num, 0x0D)
        self.write_data(num, 0x0B)
        self.write_data(num, 0x1F)
        self.write_data(num, 0x23)

        self.write_cmd(num, 0xE1)
        self.write_data(num, 0xD0)
        self.write_data(num, 0x04)
        self.write_data(num, 0x0C)
        self.write_data(num, 0x11)
        self.write_data(num, 0x13)
        self.write_data(num, 0x2C)
        self.write_data(num, 0x3F)
        self.write_data(num, 0x44)
        self.write_data(num, 0x51)
        self.write_data(num, 0x2F)
        self.write_data(num, 0x1F)
        self.write_data(num, 0x1F)
        self.write_data(num, 0x20)
        self.write_data(num, 0x23)
        
        self.write_cmd(num, 0x21)

        self.write_cmd(num, 0x11)

        self.write_cmd(num, 0x29)

        time.sleep_ms(100)

    def write_cmd(self, num, cmd):
        pass
        
    def write_data(self, num, val):
        pass
        
    def write_buffer(self, num, buf):
        pass

    def show(self, num, xStart, yStart, xEnd, yEnd, buffer):
        x = 52
        y = 40

        self.write_cmd(num, 0x2A)
        self.write_data(num, ((xStart+x) >> 8) & 0xff)        #Set the horizontal starting point to the high octet
        self.write_data(num, (xStart+x) & 0xff)    #Set the horizontal starting point to the low octet
        self.write_data(num, ((xEnd-1+x)>>8) & 0xff)        #Set the horizontal end to the high octet
        self.write_data(num, (xEnd-1+x) & 0xff)  #Set the horizontal end to the low octet 

        self.write_cmd(num, 0x2B)
        self.write_data(num, ((yStart+y) >> 8) & 0xff)
        self.write_data(num, (yStart+y) & 0xff)
        self.write_data(num, ((yEnd+y-1) >> 8) & 0xff)
        self.write_data(num, (yEnd+y-1) & 0xff)

        self.write_cmd(num, 0x2C)

        self.write_buffer(num, buffer)
