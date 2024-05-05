from machine import SPI
from spibus import SPIBus

class SPIPico(SPIBus):
    def __init__(self, bus, sck_pin, mosi_pin, miso_pin):
        super().__init__()
        self.spi = SPI(bus, baudrate=100_000_000, polarity=0, phase=0, bits=8, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)

    def send(self, cmd):
        self.spi.write(bytearray(cmd))
    
    def recv(self, n_byte):
        return self.spi.read(n_byte, 0)
    
    def transferer(self, cmd, n_byte):
        raise NotImplementedError
