from piabus import PiaBus
import framebuf, time
from piapico import PiaPico

TEMPO = 0

class Matrice(framebuf.FrameBuffer):
    def __init__(self, matrice):
        self.width = 5
        self.height = 2
        self.matrice = matrice
        self.buffer = bytearray(16 * self.height * 24 * self.width >> 3)
        super().__init__(self.buffer, 16 * self.width, 24 * self.height, framebuf.MONO_HMSB)

    def show(self):
        for j in range(self.height):
            for i in range(self.width):
                self.matrice[i*self.width].write_led_buffer(j*16*self.width, self.buffer[2*i:2*i-1])

class HC1632:
    def __init__(self, data_pin, write_pin, cs_pin, master_mode):
        self._data_pin = data_pin
        self._write_pin = write_pin
        self._cs_pin = cs_pin
        self.widthb= 16
        self.height = 24

        self._write_pin.setOutput(1)
        self._data_pin.setOutput(0)
        self._cs_pin.setOutput(1)

        self.__init_matrix__(master_mode)

    def __write_chipselect__(self, valeur):
        if valeur == 0:
            self._cs_pin.setOutput(1)
        else:
            self._cs_pin.setOutput(0)
        time.sleep_ms(TEMPO)

    def __write_bit__(self, valeur):
        self._write_pin.setOutput(0)
        #time.sleep_ms(TEMPO_1_2)

        self._data_pin.setOutput(valeur)
#         time.sleep_ms(TEMPO_1_2)
        time.sleep_ms(TEMPO)

        self._write_pin.setOutput(1)
        time.sleep_ms(TEMPO)

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

    def write_led_pixel(self, address, buffer):
        self.__write_chipselect__(1)
        self.__write_bit__(1)
        self.__write_bit__(0)
        self.__write_bit__(1)
        # address
        for i in range(7):
            self.__write_bit__(address & (1<<(6-i)))
        # data
        for i in range(4):
            self.__write_bit__(buffer & (1<<i))
        self.__write_chipselect__(0)

    def __init_matrix__(self, master_mode):
        # SYS DIS
        self.__write_sys__(0)
        time.sleep_ms(TEMPO)
        
        # COM OPTION
        self.__write_com_option__(1)
        time.sleep_ms(TEMPO)
        
        # MASTER MODE
        self.__write_mode__(master_mode)
        time.sleep_ms(TEMPO)
        
        # SYS ON
        self.__write_sys__(1)
        time.sleep_ms(TEMPO)
        
        # LED ON
        self.__write_led__(1)
        time.sleep_ms(TEMPO)
        
        self.__write_blink__(0)
        time.sleep_ms(TEMPO)
        
        self.__write_led_pwm__(0x0F)
        time.sleep_ms(TEMPO)

data_pin = PiaPico(8)
write_pin = PiaPico(9)
cs_pin = []
cs_pin.append(PiaPico(10))
cs_pin.append(PiaPico(11))
cs_pin.append(PiaPico(12))
cs_pin.append(PiaPico(13))
cs_pin.append(PiaPico(14))
cs_pin.append(PiaPico(15))

matrice = []
matrice.append(HC1632(data_pin, write_pin, cs_pin[0], 1))
for i in range(1, len(cs_pin)):
    matrice.append(HC1632(data_pin, write_pin, cs_pin[i], 0))

paint = Matrice(matrice)
# paint.fill(0)
# paint.show()
# paint.text("Loulou", 0, 0)
# paint.show()
# for y in range(paint.height):
#     for x in range(paint.width):
#         paint.pixel(x, y, 1)
#         paint.show()
#         time.sleep_ms(1)
