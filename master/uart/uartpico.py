from machine import UART
from interface.uartbus import UartBus
from machine import Pin

class UartPico(UartBus):
    def init(self, bus, bdrate, pinTx, pinRx):
        self.uart = UART(bus, baudrate=bdrate, tx=Pin(pinTx), rx=Pin(pinRx))
        self.uart.init(bdrate, bits=8, parity=None, stop=1)
        
    def send(self, cmd):
        self.uart.write(cmd)

    def recv(self, n_byte):
        rxData = self.uart.read(n_byte)
        return rxData

    def transfert(self, cmd, n_byte):
        self.send(cmd)
        return self.recv(n_byte)
