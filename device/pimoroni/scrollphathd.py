from is31fl3731 import IS31FL3731
import framebuf

class ScrollPHatHd(framebuf.FrameBuffer):
    def __init__(self, matrice):
        self.width = 17
        self.height = 7
        self.pages = 8
        self.matrice = matrice
        self.buffer = bytearray(self.width * self.height)
        super().__init__(self.buffer, self.width, self.height, framebuf.GS8)

    def show(self):
        self.matrice.pwmRegister(buffer)
