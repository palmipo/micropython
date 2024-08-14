import framebuf, time
from device.hc1632.hc1632 import HC1632

class Hc1632Matrix(framebuf.FrameBuffer):
    def __init__(self, largeur, hauteur, data_pin, write_pin, cs_pin):
        self.hauteur = hauteur
        self.largeur = largeur
        self.buffer = bytearray((HC1632.WIDTH * self.largeur * HC1632.HEIGHT * self.hauteur) >> 3)
        super().__init__(self.buffer, HC1632.WIDTH * self.largeur, HC1632.HEIGHT * self.hauteur, framebuf.MONO_HMSB)

        self.matrice = []
        self.matrice.append(HC1632(data_pin, write_pin, cs_pin[0], 1))
        for i in range(1, len(cs_pin)):
            self.matrice.append(HC1632(data_pin, write_pin, cs_pin[i], 0))
    
    def show(self):
        for j in range(self.hauteur):
            for y in range(HC1632.HEIGHT):
                for i in range(self.largeur):
                    index = (HC1632.WIDTH >> 3) * i + ((HC1632.WIDTH * self.largeur) >> 3) * y + ((HC1632.HEIGHT * HC1632.WIDTH * self.largeur) >> 3) * j
                    self.matrice[i+self.largeur*j].write_led_buffer((HC1632.WIDTH>>2)*y, self.buffer[index:index+2])
