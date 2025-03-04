import machine, time

class RS485:
    def __init__(self, aux_pin, uart):
        self.aux_pin = aux_pin
        self.uart = uart

        self.aux_pin.value(0)
        time.sleep_ms(50)

    def write(self, data):
        self.aux_pin.value(1)
        time.sleep_ms(1)

        self.uart.write(data)
        time.sleep_ms(200)

    def read(self, nb):
        self.aux_pin.value(0)
        time.sleep_ms(1)

        return self.uart.read(nb)

if __name__ == "__main__":
    aux_pin = machine.Pin(5, machine.Pin.OUT)
    uart = machine.UART(1, baudrate=9600, tx=2, rx=3)
    uart.init(9600, bits=8, parity=None, stop=1)

    rs = RS485(aux_pin, uart)
    
    while True:
        time.sleep_ms(10)
        print(rs.read(120))


