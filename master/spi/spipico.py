from machine import SPI
from spibus import SPIBus

class SPIPico(SPIBus):
    def __init__(self, bus, sck_pin, mosi_pin, miso_pin):
        super().__init__()
        self.spi = SPI(bus, baudrate=8000000, polarity=0, phase=0, bits=8, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)

    def send(self, cmd):
#         print(cmd)
        self.spi.write(cmd)
    
    def recv(self, n_byte):
        return self.spi.read(n_byte, 0)

if __name__=='__main__':
    spi = SPIPico(1, 10, 11, None)
    data = bytearray(1)
    data[0] = 0xff
    spi.send(data)
