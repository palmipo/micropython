import machine
from interface.spibus import SpiBus

class SpiPico(SpiBus):
    def __init__(self, bus, sck, mosi, miso):
        super().__init__()
        self.spi = machine.SPI(bus, baudrate=8000000, polarity=0, phase=0, bits=8, sck=sck, mosi=mosi, miso=miso)

    def send(self, txdata):
        self.spi.write(txdata)
    
    def recv(self, n_byte):
        return self.spi.read(n_byte, 0x00)

    def transferer(self, txdata):
        rxdata = bytearray(len(txdata))
        self.spi.write_readinto(txdata, rxdata)
        return rxdata
