from devicei2c import DeviceI2C
import time
 

class SSD1306(DeviceI2C):
    def __init__(self, width, height, addr, bus):
        super().__init__(0x3C | (addr & 0x01), bus)

        self.height = height
        self.width = width
        self.temp = bytearray(2)

    def init_display(self):
        self.write_cmd(0xAE)

        self.write_cmd(0x02)
        self.write_cmd(0x10)
    
        self.write_cmd(0x40)
        
        self.write_cmd(0x81)
        self.write_cmd(0x80)
        
        self.write_cmd(0xA1)
        
        self.write_cmd(0xA6)
        
        self.write_cmd(0xA8)
        self.write_cmd(self.height - 1)
        
        self.write_cmd(0xC8)
        
        self.write_cmd(0xD3)
        self.write_cmd(0x00)
        
        self.write_cmd(0xD5)
        self.write_cmd(0xF0)
        
        self.write_cmd(0xD8)
        self.write_cmd(0x05)
        
        self.write_cmd(0xD9)
        self.write_cmd(0xC2)
        
        self.write_cmd(0xDA)
        self.write_cmd(0x12)
        
        self.write_cmd(0xDB)
        self.write_cmd(0x08)
        
        self.write_cmd(0xAF)

    def show(self, buffer):
        for page in range(0, self.height >> 3): #8):
            self.write_cmd(0xB0 + page)
            self.write_cmd(0x02)
            self.write_cmd(0x10)
            for num in range(0, self.width):
                self.write_data(buffer[page * self.width + num])

    def setDisplayON(self):
        self.write_cmd(0xAF)

    def setDisplayOFF(self):
        self.write_cmd(0xAE)
        
    def write_cmd(self, cmd):
        self.temp[0] = 0x00
        self.temp[1] = cmd
        self.busi2c.send(self.adresse, self.temp)

    def write_data(self, buf):
        self.temp[0] = 0x40
        self.temp[1] = buf
        self.busi2c.send(self.adresse, self.temp)
