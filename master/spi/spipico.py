import machine
from interface.spibus import SPIBus

class SPIPico(SPIBus):
    def __init__(self, bus, sck_pin, mosi_pin, miso_pin):
        super().__init__()
        self.spi = machine.SPI(bus, baudrate=8000000, polarity=0, phase=0, bits=8, sck=machine.Pin(sck_pin), mosi=machine.Pin(mosi_pin), miso=machine.Pin(miso_pin))

    def send(self, cmd):
        self.spi.write(cmd)
    
    def recv(self, n_byte):
        return self.spi.read(n_byte, 0)
