from device.i2c.ssd1306 import SSD1306
import time
 

class OLED_0inch91(SSD1306):
    def __init__(self, addr, bus):
        super().__init__(128, 32, addr, bus)

    def init_display(self):
        self.__write_cmd__(0xAE)

        self.__write_cmd__(0x40) # set low column address
        self.__write_cmd__(0xB0) # set high column address

        self.__write_cmd__(0xC8) # not offset

        self.__write_cmd__(0x81)
        self.__write_cmd__(0xff)

        self.__write_cmd__(0xa1)

        self.__write_cmd__(0xa6)

        self.__write_cmd__(0xa8)
        self.__write_cmd__(0x1f)

        self.__write_cmd__(0xd3)
        self.__write_cmd__(0x00)

        self.__write_cmd__(0xd5)
        self.__write_cmd__(0xf0)

        self.__write_cmd__(0xd9)
        self.__write_cmd__(0x22)

        self.__write_cmd__(0xda)
        self.__write_cmd__(0x02)

        self.__write_cmd__(0xdb)
        self.__write_cmd__(0x49)

        self.__write_cmd__(0x8d)
        self.__write_cmd__(0x14) 

    def show(self, buffer):
        for page in range(0, self.height >> 3):
            self.__write_cmd__(0xB0 + page)
            self.__write_cmd__(0x00)
            self.__write_cmd__(0x10)
            for num in range(0, self.width):
                self.__write_data__(buffer[page * self.width + num])

# from i2cpico import I2CPico
# import framebuf
# import time
# 
# 
# i2c = I2CPico(0, 4, 5)
# print(hex(i2c.scan()[0]))
#  
# 
# width = 128
# height = 32
# 
# buffer = bytearray(width * (height >> 3))
# 
# display = OLED_0_91(width, height, 0, i2c)
# display.init_display()
# display.setDisplayON()
# display.setEntireDisplayON()
# time.sleep(1)
# display.setEntireDisplayOFF()
# 
# frame = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_VLSB)
# frame.text('192.168.001.xxx', 0, 0)
# display.show(buffer)
# 
# time.sleep(5)
# display.setDisplayOFF()
