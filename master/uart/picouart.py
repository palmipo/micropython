from machine import UART, Pin
from busuart import BusUart

class PicoUart(BusUart):
    def __init__(self, bdrate):
        self.__uart = UART(0, baudrate = bdrate, tx=Pin(0), rx=Pin(1))
        
    def send(self, cmd):
        self.__uart.write(cmd)

    def recv(self, n_byte):
        rxData = self.__uart.read(n_byte)
        return rxData

    def transfer(self, cmd, n_byte):
        self.send(cmd)
        return self.recv(n_byte)
