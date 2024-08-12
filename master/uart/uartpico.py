from machine import UART
from interface.uartbus import UartBus
from machine import Pin

class UartPico(UartBus):
    def __init__(self, bus, bdrate, pinTx, pinRx):
        self.__uart = UART(bus, baudrate=bdrate, tx=Pin(pinTx), rx=Pin(pinRx))
        self.__uart.init(bdrate, bits=8, parity=None, stop=1)
        
    def send(self, cmd):
        self.__uart.write(cmd)
        print(cmd)

    def recv(self, n_byte):
        rxData = self.__uart.read(n_byte)
        return rxData

    def transfert(self, cmd, n_byte):
        self.send(cmd)
        return self.recv(n_byte)
