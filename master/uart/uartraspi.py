import serial
from interface.uartbus import UartBus

class UartRaspi(UartBus):
    def __init__(self, device, bdrate):
        self.__uart = serial.Serial(bus, baudrate=bdrate, timeout=3.0)
        self.__uart.init(bdrate, bits=8, parity=None, stop=1)
        
    def send(self, cmd):
        self.__uart.write(cmd)

    def recv(self, n_byte):
        rxData = self.__uart.read(n_byte)
        return rxData

    def recv(self):
        rxData = self.__uart.readline()
        return rxData

    def transfert(self, cmd, n_byte):
        self.send(cmd)
        return self.recv(n_byte)


raspi = UartRaspi("/dev/ttyAMA0", 115200)
