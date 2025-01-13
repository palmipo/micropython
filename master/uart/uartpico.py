import machine
from interface.uartbus import UartBus

class UartPico(UartBus):
    def init(self, bus, bdrate, pinTx, pinRx):
        self.uart = machine.UART(bus, baudrate=bdrate, tx=machine.Pin(pinTx), rx=machine.Pin(pinRx))
        self.uart.init(bdrate, bits=8, parity=None, stop=1)
        
    def send(self, cmd):
        self.uart.write(cmd)

    def recv(self, n_byte):
        rxData = self.uart.read(n_byte)
        return rxData

    def transfert(self, cmd, n_byte):
        self.send(cmd)
        return self.recv(n_byte)
