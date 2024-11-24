import socket
from interface.socketbus import SocketBus

class SocketTcp(SocketBus):
    def __init__(self):
        super.__init__()

    def serveur(self, port):
        self.connect("0.0.0.0", port)
        self.__socket__.bind(port)
        self.__socket__.listen()
        self.__socket__.accept()
    
    def client(self, adresse, port):
        self.connect(adresse, port)
        
    def connect(self, adresse, port):
        self.__socket__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket__.connect(socket.getaddrinfo(adresse, port)[0][-1])

    def disconnect(self):
        self.__socket.close()

    def send(self, cmd):
        self.__socket__.send(cmd)

    def recv(self, n_byte):
        rsp = self.__socket__.recv(n_byte)
        return rsp

    def transferer(self, cmd, n_byte):
        self.__socket__.send(cmd)
        rsp = self.__socket__.recv(n_byte)
        return rsp