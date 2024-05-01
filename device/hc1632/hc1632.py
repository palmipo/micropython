from piabus import PiaBus
import time

class HC1632:
    WIDTH = 16
    HEIGHT = 24
    TEMPO = 10

    def __init__(self, data_pin, write_pin, cs_pin, master_mode):
        self._data_pin = data_pin
        self._write_pin = write_pin
        self._cs_pin = cs_pin

        self._write_pin.set(1)
        self._data_pin.set(1)
        self._cs_pin.set(1)

        self.__init_matrix__(master_mode)

    def __write_chipselect__(self, valeur):
        if valeur == 0:
            self._cs_pin.set(1)
        else:
            self._cs_pin.set(0)
        time.sleep_us(HC1632.TEMPO)

    def __write_bit__(self, valeur):
        self._write_pin.set(0)
        
        if valeur != 0:
            self._data_pin.set(1)
        else:
            self._data_pin.set(0)
        time.sleep_us(HC1632.TEMPO)

        self._write_pin.set(1)
        time.sleep_us(HC1632.TEMPO)

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
        time.sleep_us(HC1632.TEMPO)
        
        # COM OPTION
        self.__write_com_option__(1)
        time.sleep_us(HC1632.TEMPO)
        
        # MASTER MODE
        self.__write_mode__(master_mode)
        time.sleep_us(HC1632.TEMPO)
        
        # SYS ON
        self.__write_sys__(1)
        time.sleep_us(HC1632.TEMPO)
        
        # LED ON
        self.__write_led__(1)
        time.sleep_us(HC1632.TEMPO)
        
        self.__write_blink__(0)
        time.sleep_us(HC1632.TEMPO)
        
        self.__write_led_pwm__(0x07)
        time.sleep_us(HC1632.TEMPO)
