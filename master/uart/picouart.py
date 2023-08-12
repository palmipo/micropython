from machine import UART, Pin
from busuart import BusUart

class PicoUart(BusUart):
    def __init__(self, bdrate):
        self.__uart = UART(0, baudrate = bdrate, tx=Pin(0), rx=Pin(1))
        
    def send(self, cmd):
        #self.__uart.write(cmd)
        print(cmd)

    def recv(self, n_byte):
        #rxData = self.__uart.read(n_byte)
        rxData = bytearray(b'\x01\x03\x01\x00\x00\x00\x00\x00')
        return rxData

    def transferer(self, cmd, n_byte):
        self.send(cmd)
        return self.recv(n_byte)
