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
        self.dc_pin = PiaPicoOutput(20)
        self.busy_pin = PiaPicoInput(22)
        self.cs_pin = PiaPicoOutput(17)
        self.spi = SPIPico(0, 18, 19, None)

        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.BLACK  = 0x000000   #   00  BGR
        self.WHITE  = 0xffffff   #   01
        self.YELLOW = 0x00ffff   #   10
        self.RED    = 0x0000ff   #   11
        
    # Hardware reset
    def reset(self):
        self.reset_pin.set(1)
        time.sleep_ms(200) 
        self.reset_pin.set(0)         # module reset
        time.sleep_ms(2)
        self.reset_pin.set(1)
        time.sleep_ms(200)   

    def send_command(self, command):
        self.dc_pin.set(0)
        self.cs_pin.set(0)
        self.spi.send(command)
        self.cs_pin.set(1)

    def send_data(self, data):
        self.dc_pin.set(1)
        self.cs_pin.set(0)
        self.spi.send(data)
        self.cs_pin.set(1)

    def send_buffer(self, data):
        self.dc_pin.set(1)
        self.cs_pin.set(0)
        for d in data:
            self.spi.send(d)
        self.cs_pin.set(1)

    def ReadBusyH(self):
        while(self.busy_pin.get() == 0):      # 0: idle, 1: busy
            time.sleep_ms(5)

    def ReadBusyL(self):
        while(self.busy_pin.get() == 1):      # 0: busy, 1: idle
            time.sleep_ms(5)

    def TurnOnDisplay(self):
        self.send_command(b'0x12') # DISPLAY_REFRESH
        self.send_data(b'0x01')
        self.ReadBusyH()

        self.send_command(b'0x02') # POWER_OFF
        self.send_data(b'0X00')
        self.ReadBusyH()
        
    def init(self):
        self.reset()

        self.send_command(b'0x66')
        self.send_data(b'0x49')
        self.send_data(b'0x55')
        self.send_data(b'0x13')
        self.send_data(b'0x5D')

        self.send_command(b'0x66')
        self.send_data(b'0x49')
        self.send_data(b'0x55')

        self.send_command(b'0xB0')
        self.send_data(b'0x03')

        self.send_command(b'0x00')
        self.send_data(b'0x4F')
        self.send_data(b'0x69')

        self.send_command(b'0x03')
        self.send_data(b'0x00')

        self.send_command(b'0xF0')
        self.send_data(b'0xF6')
        self.send_data(b'0x0D')
        self.send_data(b'0x00')
        self.send_data(b'0x00')
        self.send_data(b'0x00')

        self.send_command(b'0x06')
        self.send_data(b'0xCF')
        self.send_data(b'0xDE')
        self.send_data(b'0x0F')

        self.send_command(b'0x41')
        self.send_data(b'0x00')

        self.send_command(b'0x50')
        self.send_data(b'0x30')

        self.send_command(b'0x60')
        self.send_data(b'0x0C') 
        self.send_data(b'0x05')

        self.send_command(b'0x61')
        self.send_data(b'0xA8')
        self.send_data(b'0x01') 
        self.send_data(b'0x28') 

        self.send_command(b'0x84')
        self.send_data(b'0x01')
        return 0

#     def getbuffer(self, image):
#         # Create a pallette with the 4 colors supported by the panel
#         pal_image = Image.new("P", (1,1))
#         pal_image.putpalette( (0,0,0,  255,255,255,  255,255,0,   255,0,0) + (0,0,0)*252)
# 
#         # Check if we need to rotate the image
#         imwidth, imheight = image.size
#         if(imwidth == self.width and imheight == self.height):
#             image_temp = image
#         elif(imwidth == self.height and imheight == self.width):
#             image_temp = image.rotate(90, expand=True)
#         else:
#             logger.warning("Invalid image dimensions: %d x %d, expected %d x %d" % (imwidth, imheight, self.width, self.height))
# 
#         # Convert the soruce image to the 4 colors, dithering if needed
#         image_4color = image_temp.convert("RGB").quantize(palette=pal_image)
#         buf_4color = bytearray(image_4color.tobytes('raw'))
# 
#         # into a single byte to transfer to the panel
#         buf = [0x00] * int(self.width * self.height / 4)
#         idx = 0
#         for i in range(0, len(buf_4color), 4):
#             buf[idx] = (buf_4color[i] << 6) + (buf_4color[i+1] << 4) + (buf_4color[i+2] << 2) + buf_4color[i+3]
#             idx += 1
# 
#         return buf

    def display(self, image):
        if self.width % 4 == 0 :
            Width = self.width // 4
        else :
            Width = self.width // 4 + 1
        Height = self.height

        self.send_command(b'0x68')
        self.send_data(b'0x01')

        self.send_command(b'0x04')
        self.ReadBusyH()

        self.send_command(b'0x10')
        for j in range(0, Height):
            for i in range(0, Width):
                    self.send_data(image[i + j * Width])

        self.send_command(b'0x68')
        self.send_data(b'0x00')

        self.TurnOnDisplay()
        
    def Clear(self, color=0x55):
        if self.width % 4 == 0 :
            Width = self.width // 4
        else :
            Width = self.width // 4 + 1
        Height = self.height

        self.send_command(b'0x68')
        self.send_data(b'0x01')

        self.send_command(b'0x04')
        self.ReadBusyH()

        self.send_command(b'0x10')
        for j in range(0, Height):
            for i in range(0, Width):
                self.send_data(color)

        self.send_command(b'0x68')
        self.send_data(b'0x00')

        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(b'0x02') # POWER_OFF
        self.send_data(b'0x00')

        self.send_command(b'0x07') # DEEP_SLEEP
        self.send_data(b'0XA5')
    

if __name__ == '__main__':
    try:
        display = EPD()
        display.init()
        
        buffer = bytearray((display.width//4) * display.height)
        frame = framebuf.FrameBuffer(buffer, display.width, display.height, framebuf.GS2_HMSB)
        frame.fill(display.BLACK)
        
        display.display(buffer)
        display.sleep()

    except KeyboardInterrupt:
        sys.exit()
