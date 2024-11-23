import machine
from interface.spibus import SpiBus

class SpiPico(SpiBus):
    def __init__(self, bus, sck_pin, mosi_pin, miso_pin):
        super().__init__()
        self.spi = machine.SPI(bus, baudrate=8000000, polarity=0, phase=0, bits=8, sck=machine.Pin(sck_pin), mosi=machine.Pin(mosi_pin), miso=machine.Pin(miso_pin))

    def send(self, txdata):
        self.spi.write(txdata)
    
    def recv(self, n_byte):
        return self.spi.read(n_byte, 0x00)

    def transferer(self, txdata):
        rxdata = bytearray(len(txdata))
        self.spi.write_readinto(txdata, rxdata)
        return rxdata
