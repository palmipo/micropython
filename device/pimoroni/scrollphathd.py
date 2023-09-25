from is31fl3731 import IS31FL3731
import framebuf
import time

class ScrollPHatHd(framebuf.FrameBuffer):
    def __init__(self, i2c):
        self.width = 8
        self.height = 18
        self.buffer = bytearray(self.width * self.height)
        super().__init__(self.buffer, self.width, self.height, framebuf.GS8)

        self.matrix = IS31FL3731(0, i2c)
        self.matrix.shutdown(1)
        time.sleep(1)

        self.matrix.configurationRegister(0, 0)
        self.matrix.pictureDisplayRegister(0)
        self.matrix.displayOptionRegister(0, 0, 0)
        self.matrix.autoplayControlRegister(0, 0, 0)
        self.matrix.breathControlRegister(0, 0, 0, 0)

        self.led = bytearray(18)
        self.blink = bytearray(18)
        pwm = bytearray(144)

        for i in range(0, 18):
            self.led[i] = 0xff
            self.blink[i] = 0

        for i in range(0, 144):
            pwm[i]=0

        for i in range(0, 8):
            self.matrix.frameRegister(i, self.led, self.blink, pwm)

    def show(self):
        self.matrix.pageRegister(0)
        self.matrix.pwmRegister(self.buffer)
