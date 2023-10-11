import socket

class SocketUdp(SocketBus):
    def __init__(self):
        super.__init__()

    def connection(self, adresse, port):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.connect(socket.getaddrinfo(adresse, port)[0][-1])

    def disconnection(self):
        self.__socket.close()

    def send(self, cmd):
        self.__socket.send(cmd)

    def recv(self, n_byte):
        rsp = self.__socket.recv(n_byte)
        return rsp

    def transfer(self, cmd, n_byte):
        self.__socket.send(cmd)
        rsp = self.__socket.recv(n_byte)
        return rsp