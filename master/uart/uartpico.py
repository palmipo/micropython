from machine import UART
from uartbus import UartBus

class UartPico(UartBus):
    def __init__(self, bus):
        self.__uart = UART(bus, baudrate=9600)
        self.__uart.init(9600, bits=8, parity=None, stop=1)
        
    def send(self, cmd):
        self.__uart.write(cmd)

    def recv(self, n_byte):
        rxData = self.__uart.read(n_byte)
        return rxData

    def transfer(self, cmd, n_byte):
        self.send(cmd)
        return self.recv(n_byte)
