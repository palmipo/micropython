from piabus import PiaBus
import framebuf

int32_t TEMPO = 100
int32_t TEMPO_1_2 = 50

class Matrice(framebuf.FrameBuffer):
    def __init__(self, width, height, HC1632List):
        self.width = width
        self.height = height
        self.buffer = bytearray(self.height * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)

    def show(self):
        for HC1632 matrice in HC1632List:
            matrice.write_led_buffer()

class HC1632:
    def __init__(self, data_pin, write_pin, cs_pin, master_mode):
        self._data_pin = data_pin
        self._write_pin = write_pin
        self._cs_pin = cs_pin

        self._write_pin.setOutput(1)
        self._data_pin.setOutput(1)
        self._cs_pin.setOutput(1)

        self.init(master_mode)

    def write_chipselect(self, valeur):
        self._cs_pin.setOutput(valeur?0:1)
        time.sleep_ms(TEMPO)

    def write_bit(valeur):
        self._write_pin.setOutput(0)
        time.sleep_ms(TEMPO_1_2)
        self._data_pin.setOutput(valeur?1:0)
        time.sleep_ms(TEMPO_1_2)
        self._write_pin.setOutput(1)
        time.sleep_ms(TEMPO)

    def write_sys(on):
        write_chipselect(1)
        write_bit(1)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(on)
        write_bit(0)
        write_chipselect(0)

    def write_com_option(config):
        write_chipselect(1)
        write_bit(1)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(1)
        write_bit(0)
        write_bit(config & 0x02) // a
        write_bit(config & 0x01) // b
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_chipselect(0)

    def write_mode(mode):
        write_chipselect(1)
        write_bit(1)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(1)
        write_bit(mode)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_chipselect(0)

    def write_led(on):
        write_chipselect(1)
        write_bit(1)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(1)
        write_bit(on)
        write_bit(0)
        write_chipselect(0)

    def write_blink(on):
        write_chipselect(1)
        write_bit(1)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(1)
        write_bit(0)
        write_bit(0)
        write_bit(on)
        write_bit(0)
        write_chipselect(0)

    def write_led_pwm(intensity):
        write_chipselect(1)
        write_bit(1)
        write_bit(0)
        write_bit(0)
        write_bit(1)
        write_bit(0)
        write_bit(1)
        write_bit(0)
        write_bit(intensity & 0x08)
        write_bit(intensity & 0x04)
        write_bit(intensity & 0x02)
        write_bit(intensity & 0x01)
        write_bit(0)
        write_chipselect(0)

    def write_led_buffer(buffer)
        write_chipselect(1)
        write_bit(1)
        write_bit(0)
        write_bit(1)
        /* address */
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        write_bit(0)
        /* data */
        for octet in buffer:
            for i in range(8):
                write_bit((octet & (1<<i)) >> i)
        write_chipselect(0)

    def write_led_pixel(quartet, buffer):
        write_chipselect(1)
        write_bit(1)
        write_bit(0)
        write_bit(1)
        /* address */
        for (int32_t i=0 i<7 ++i)
            write_bit(quartet & (1<<(6-i)))
        /* data */
        for (int32_t i=0 i<4 ++i)
            write_bit(buffer & (1<<i))
        write_chipselect(0)

    def init(master_mode):
        // SYS DIS
        write_sys(0)
        time.sleep_ms(TEMPO)
        // COM OPTION
        write_com_option(1)
        time.sleep_ms(TEMPO)
        // MASTER MODE
        write_mode(master_mode)
        time.sleep_ms(TEMPO)
        // SYS ON
        write_sys(1)
        time.sleep_ms(TEMPO)
        // LED ON
        write_led(1)
        time.sleep_ms(TEMPO)
        write_blink(0)
        time.sleep_ms(TEMPO)
        write_led_pwm(0x0F)
        time.sleep_ms(TEMPO)

