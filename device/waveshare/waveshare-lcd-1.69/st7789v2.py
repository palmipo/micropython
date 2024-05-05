import time

class ST7789V2:
    def __init__(self):
        self.reset()

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

        time.sleep_ms(100)

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

        self.write_buffer(buffer)

    def write_cmd(self, cmd):
        pass

    def write_data(self, buf):
        pass

    def write_buffer(self, buf):
        pass

    def write_brightness(self, val):
        pass
    
    def reset(self):
        pass
