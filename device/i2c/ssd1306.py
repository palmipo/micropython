from devicei2c import DeviceI2C
import time
 

class SSD1306(DeviceI2C):
    def __init__(self, width, height, addr, bus):
        super().__init__(0x3C | (addr & 0x01), bus)

        self.height = height
        self.width = width
        self.temp = bytearray(2)

    def setDisplayON(self):
        self.__write_cmd__(0xAF)

    def setDisplayOFF(self):
        self.__write_cmd__(0xAE)

    def setEntireDisplayON(self):
        self.__write_cmd__(0xA5)

    def setEntireDisplayOFF(self):
        self.__write_cmd__(0xA4)
        
    def __write_cmd__(self, cmd):
        self.temp[0] = 0x00
        self.temp[1] = cmd
        self.busi2c.send(self.adresse, self.temp)

    def __write_data__(self, buf):
        self.temp[0] = 0x40
        self.temp[1] = buf
        self.busi2c.send(self.adresse, self.temp)
