from ssd1306 import SSD1306
import time
 

class OLED_1_3(SSD1306):
    def __init__(self, addr, bus):
        super().__init__(128, 64, addr, bus)

    def init_display(self):
        self.__write_cmd__(0xAE)

        self.__write_cmd__(0x02)
        self.__write_cmd__(0x10)
    
        self.__write_cmd__(0x40)
        
        self.__write_cmd__(0x81)
        self.__write_cmd__(0x80)
        
        self.__write_cmd__(0xA1)
        
        self.__write_cmd__(0xA6)
        
        self.__write_cmd__(0xA8)
        self.__write_cmd__(self.height - 1)
        
        self.__write_cmd__(0xC8)
        
        self.__write_cmd__(0xD3)
        self.__write_cmd__(0x00)
        
        self.__write_cmd__(0xD5)
        self.__write_cmd__(0xF0)
        
        self.__write_cmd__(0xD8)
        self.__write_cmd__(0x05)
        
        self.__write_cmd__(0xD9)
        self.__write_cmd__(0xC2)
        
        self.__write_cmd__(0xDA)
        self.__write_cmd__(0x12)
        
        self.__write_cmd__(0xDB)
        self.__write_cmd__(0x08)

    def show(self, buffer):
        for page in range(0, self.height >> 3):
            self.__write_cmd__(0xB0 + page)
            self.__write_cmd__(0x02)
            self.__write_cmd__(0x10)
            for num in range(0, self.width):
                self.__write_data__(buffer[page * self.width + num])

