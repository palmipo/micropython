from master.pia.piapico import PiaPicoInput
from master.pia.piapico import PiaPicoOutput
from master.spi.spipico import SPIPico
import time
import framebuf

# Display resolution
EPD_WIDTH  = 168
EPD_HEIGHT = 296


class EPD:
    def __init__(self):
        self.reset_pin = PiaPicoOutput(21)
        self.reset_pin.set(1)
        self.dc_pin = PiaPicoOutput(20)
        self.busy_pin = PiaPicoInput(22)
        self.cs_pin = PiaPicoOutput(17)
        self.cs_pin.set(1)

        self.spi = SPIPico(0, 18, 19, None)

        self.dc_pin.set(1)

        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    # Hardware reset
    def reset(self):
        self.reset_pin.set(0)         # module reset
        time.sleep_ms(2)
        self.reset_pin.set(1)
        time.sleep_ms(20)   

    def send_command(self, command):
        self.dc_pin.set(0)
        self.cs_pin.set(0)
        buf = bytearray(1)
        buf[0] = command
        self.spi.send(buf)
        self.cs_pin.set(1)

    def send_data(self, data):
        self.dc_pin.set(1)
        self.cs_pin.set(0)
        buf = bytearray(1)
        buf[0] = data
        self.spi.send(buf)
        self.cs_pin.set(1)

    def send_buffer(self, data):
        self.dc_pin.set(1)
        self.cs_pin.set(0)
        buf = bytearray(1)
        for i in range(0,len(data)):
            buf[0] = data[i]
            self.spi.send(buf)
        self.cs_pin.set(1)

    def ReadBusyH(self):
        while(self.busy_pin.get() == 0):      # 0: idle, 1: busy
            time.sleep_ms(5)

    def ReadBusyL(self):
        while(self.busy_pin.get() == 1):      # 0: busy, 1: idle
            time.sleep_ms(5)

    def TurnOnDisplay(self):
        self.send_command(0x12) # DISPLAY_REFRESH
        self.send_data(0x00)#(0x01)
        self.ReadBusyH()

        self.send_command(0x02) # POWER_OFF
        self.send_data(0X00)
        self.ReadBusyH()
        
    def init(self):
        self.reset()

        self.send_command(0x66)
        self.send_data(0x49)
        self.send_data(0x55)
        self.send_data(0x13)
        self.send_data(0x5D)

        self.send_command(0x66)
        self.send_data(0x49)
        self.send_data(0x55)

        self.send_command(0xB0)
        self.send_data(0x03)

        self.send_command(0x00)
        self.send_data(0x4F)
        self.send_data(0x69)

        self.send_command(0x03)
        self.send_data(0x00)

        self.send_command(0xF0)
        self.send_data(0xF6)
        self.send_data(0x0D)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x06)
        self.send_data(0xCF)
        self.send_data(0xDE)
        self.send_data(0x0F)

        self.send_command(0x41)
        self.send_data(0x00)

        self.send_command(0x50)
        self.send_data(0x30)

        self.send_command(0x60)
        self.send_data(0x0C) 
        self.send_data(0x05)

        self.send_command(0x61)
        self.send_data(0xA8)
        self.send_data(0x01) 
        self.send_data(0x28) 

        self.send_command(0x84)
        self.send_data(0x01)

    def sleep(self):
        self.send_command(0x02) # POWER_OFF
        self.send_data(0x00)

        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0XA5)

    def show(self, image):
        self.send_command(0x68)
        self.send_data(0x01)

        self.send_command(0x04)
        self.ReadBusyH()

        self.send_command(0x10)
        self.send_buffer(image)
    
        self.send_command(0x68)
        self.send_data(0x00)

        self.TurnOnDisplay()
        
    def clear(self, buffer, color=0x1):
        c = color | (color << 2) | (color << 4) | (color << 6)
        for j in range(len(buffer)):
            buffer[j] = color

        self.show(buffer)
    
    def drawPoint(self, buffer, x, y, c):
        index = x + y * self.width
	octet = index >> 3
	masque = octet - (index << 3)
        buffer[octet] = buffer[octet] & ~(0x03 << masque) | (c << masque)

    # y = ax + b
    def drawLine(self, buffer, x1, y1, x2, y2, c):
        dy = y2 - y1
        dx = x2 - x1
        a = dy // dx
        b = y1 - a * x1
        for i in range(x1, x2):
            j = a * i + b
            self.drawPoint(buffer, i, j, c)

if __name__ == '__main__':
    try:
        display = EPD()
        display.init()

        # 4 pixels par octet        
        buffer = bytearray((display.width >> 2) * display.height)
        display.clear(buffer, 0x2)
        display.drawLine(buffer, 0, 0, display.width, display.height, 0x3)
        display.drawLine(buffer, 0, display.height, display.width, 0, 0x3)
        display.show(buffer)

        time.sleep(1)
        display.sleep()

    except KeyboardInterrupt:
        display.sleep()
        sys.exit()

