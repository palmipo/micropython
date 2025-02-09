import machine, time

class APC220:
    def __init__(self, set_pin, aux_pin, en_pin, uart):
        self.set_pin = set_pin
        self.aux_pin = aux_pin
        self.en_pin = en_pin
        self.uart = uart

        self.en_pin.value(1)
        self.set_pin.value(0)
        self.aux_pin.value(0)
        time.sleep_ms(50)

# 418MHz to 455MHz (1KHz stepping)
# Frequency 6bytes Unit is KHz,for example 434MHz is 434000.
# Rf data rate 1byte 1,2,3 and 4 refer to 2400,4800,9600,19200bps separetely.
# Output power 1byte 0 to 9, 9 means 13dBm(20mW).
# UART rate 1byte 0,1,2,3,4,5 and 6 refers to 1200,2400,4800,9600,19200,38400,57600bps separately.
# Series checkout 1byte Series checkout：0 means no check,1 means even parity,2 means odd parity
    def setConfig(self, frequency=b'434000', air_rate=b'4', rf_power=b'9'):
        self.set_pin.value(0)
        time.sleep_ms(1)
        
        cmd = b'WR ' + frequency + ' ' + air_rate + ' ' + rf_power + ' 3 0\x0d\x0a'
        self.write(cmd)
        print(self.read(25))

        self.set_pin.value(1)
        time.sleep_ms(10)

    def getConfig(self):
        self.set_pin.value(0)
        time.sleep_ms(1)
        
        cmd = b'RD\x0d\x0a'
        self.write(cmd)
        print(self.read(25))

        self.set_pin.value(1)
        time.sleep_ms(10)

    def setId(self, net_id = b'00001', node_id = b'000000000001'):
        self.set_pin.value(0)
        time.sleep_ms(1)
        
        cmd = b'NET ID ' + net_id + b'\x0d\x0a'
        self.write(cmd)
        self.read(25)

        cmd = b'NODE ID ' + node_id + b'\x0d\x0a'
        self.write(cmd)
        self.read(25)

        set_pin.value(1)
        time.sleep_ms(10)

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
#     # RASPBERRY PI PICO
#     set_pin = machine.Pin(4, machine.Pin.OUT)
#     aux_pin = machine.Pin(3, machine.Pin.OUT)
#     en_pin = machine.Pin(2, machine.Pin.OUT)
#     uart = machine.UART(0, baudrate=9600, tx=0, rx=1)

    # waveshare ESP32-S2-LCD-0.96
    set_pin = machine.Pin(4, machine.Pin.OUT)
    aux_pin = machine.Pin(5, machine.Pin.OUT)
    en_pin = machine.Pin(43, machine.Pin.OUT)
    uart = machine.UART(1, baudrate=9600, tx=2, rx=3)

    uart.init(9600, bits=8, parity=None, stop=1)
    rf = APC220(set_pin, aux_pin, en_pin, uart)
    rf.getConfig()
    rf.setConfig(frequency=b'434000', air_rate=b'4', rf_power=b'9')
    
    while True:
        time.sleep_ms(10)
        print(rf.read(120))

