import serial
from interface.uartbus import UartBus

class UartRaspi(UartBus):
    def __init__(self, device, bdrate):
    # uart = serial.Serial('/dev/ttyUSB0', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=5)
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

if __name__ == "__main__":
  raspi = UartRaspi("/dev/ttyAMA0", 115200)
