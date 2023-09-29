from piabus import PiaBus
import framebuf, time
from piapico import PiaPico

TEMPO = 999

class Matrice(framebuf.FrameBuffer):
    def __init__(self, largeur, hauteur, data_pin, write_pin, cs_pin):
        self.hauteur = hauteur
        self.largeur = largeur
        self.buffer = bytearray((HC1632.largeur * largeur * HC1632.hauteur * hauteur) >> 3)
        super().__init__(self.buffer, HC1632.largeur * largeur, HC1632.hauteur * hauteur, framebuf.MONO_HMSB)

        self.matrice = []
        self.matrice.append(HC1632(data_pin, write_pin, cs_pin[0], 1))
        for i in range(1, len(cs_pin)):
            self.matrice.append(HC1632(data_pin, write_pin, cs_pin[i], 0))
    
    def show(self):
        for j in range(self.hauteur):
            for y in range(HC1632.hauteur):
                for i in range(self.largeur):
                    index = (HC1632.largeur >> 3) * i + ((HC1632.largeur * self.largeur) >> 3) * y + ((HC1632.hauteur * HC1632.largeur * self.largeur) >> 3) * j
                    print(i+self.largeur*j, (HC1632.largeur>>2)*y, index, self.buffer[index:index+2])
                    self.matrice[i+self.largeur*j].write_led_buffer((HC1632.largeur>>2)*y, self.buffer[index:index+2])

class HC1632:
    largeur = 16
    hauteur = 24
    def __init__(self, data_pin, write_pin, cs_pin, master_mode):
        self._data_pin = data_pin
        self._write_pin = write_pin
        self._cs_pin = cs_pin

        self._write_pin.setOutput(1)
        self._data_pin.setOutput(1)
        self._cs_pin.setOutput(1)

        self.__init_matrix__(master_mode)

    def __write_chipselect__(self, valeur):
        if valeur == 0:
            self._cs_pin.setOutput(1)
        else:
            self._cs_pin.setOutput(0)
        time.sleep_us(TEMPO)

    def __write_bit__(self, valeur):
        self._write_pin.setOutput(0)
        
        if valeur != 0:
            self._data_pin.setOutput(1)
        else:
            self._data_pin.setOutput(0)
        time.sleep_us(TEMPO)

        self._write_pin.setOutput(1)
        time.sleep_us(TEMPO)

    def __write_sys__(self, on):
        self.__write_chipselect__(1)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(on)
        self.__write_bit__(0)
        self.__write_chipselect__(0)

    def __write_com_option__(self, config):
        self.__write_chipselect__(1)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(config & 0x02) # a
        self.__write_bit__(config & 0x01) # b
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_chipselect__(0)

    def __write_mode__(self, mode):
        self.__write_chipselect__(1)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(1)
        self.__write_bit__(mode)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_chipselect__(0)

    def __write_led__(self, on):
        self.__write_chipselect__(1)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(1)
        self.__write_bit__(on)
        self.__write_bit__(0)
        self.__write_chipselect__(0)

    def __write_blink__(self, on):
        self.__write_chipselect__(1)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(on)
        self.__write_bit__(0)
        self.__write_chipselect__(0)

    def __write_led_pwm__(self, intensity):
        self.__write_chipselect__(1)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(0)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(intensity & 0x08)
        self.__write_bit__(intensity & 0x04)
        self.__write_bit__(intensity & 0x02)
        self.__write_bit__(intensity & 0x01)
        self.__write_bit__(0)
        self.__write_chipselect__(0)

    def write_led_buffer(self, address, buffer):
        self.__write_chipselect__(1)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(1)

        # address
        for i in range(7):
            self.__write_bit__(address & (1<<(6-i)))

        # data
        for octet in buffer:
            for i in range(8):
                self.__write_bit__((octet & (1<<i)) >> i)

        self.__write_chipselect__(0)

    def __init_matrix__(self, master_mode):
        # SYS DIS
        self.__write_sys__(0)
        time.sleep_us(TEMPO)
        
        # COM OPTION
        self.__write_com_option__(1)
        time.sleep_us(TEMPO)
        
        # MASTER MODE
        self.__write_mode__(master_mode)
        time.sleep_us(TEMPO)
        
        # SYS ON
        self.__write_sys__(1)
        time.sleep_us(TEMPO)
        
        # LED ON
        self.__write_led__(1)
        time.sleep_us(TEMPO)
        
        self.__write_blink__(0)
        time.sleep_us(TEMPO)
        
        self.__write_led_pwm__(0x0F)
        time.sleep_us(TEMPO)

data_pin = PiaPico(8)
write_pin = PiaPico(9)
cs_pin = []
cs_pin.append(PiaPico(10))
cs_pin.append(PiaPico(11))
cs_pin.append(PiaPico(12))
cs_pin.append(PiaPico(13))
cs_pin.append(PiaPico(14))
cs_pin.append(PiaPico(15))
# cs_pin.append(PiaPico(16))
# cs_pin.append(PiaPico(17))
# cs_pin.append(PiaPico(18))
# cs_pin.append(PiaPico(19))

# aff1 = HC1632(data_pin, write_pin, cs_pin[0], 1)
# aff2 = HC1632(data_pin, write_pin, cs_pin[1], 0)
# aff3 = HC1632(data_pin, write_pin, cs_pin[2], 0)
# aff4 = HC1632(data_pin, write_pin, cs_pin[3], 0)
# aff5 = HC1632(data_pin, write_pin, cs_pin[4], 0)
# aff6 = HC1632(data_pin, write_pin, cs_pin[5], 0)
# buf = bytearray(16*24>>3)
# for i in range(16*24/8):
#     buf[i] = 0xFF
# aff1.write_led_buffer(0, buf)
# aff2.write_led_buffer(0, buf)
# aff3.write_led_buffer(0, buf)
# aff4.write_led_buffer(0, buf)
# aff5.write_led_buffer(0, buf)
# aff6.write_led_buffer(0, buf)

paint = Matrice(3, 2, data_pin, write_pin, cs_pin)
paint.fill(0)
paint.show()
# paint.pixel(0, 0, 1)
# paint.pixel(0, 24, 1)
# for i in range(25):
#     paint.pixel(0, i, 1)
# paint.show()
paint.text("Loulou 1er", 0, 0)
paint.show()
