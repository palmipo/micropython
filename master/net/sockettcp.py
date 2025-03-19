from interface.socketbus import SocketBus
import socket

class SocketTcp(SocketBus):
    def __init__(self, sock=None):
        super.__init__()

        if sock == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        else:
            self.sock = sock

        self.sock.setblocking(True)

    def serveur(self, port):
        self.mode = self.SERVEUR
        self.sock.bind(port)
        self.sock.listen()

    def connect(self, adresse, port):
        self.sock.connect(socket.getaddrinfo(adresse, port)[0][-1])

    def disconnect(self):
        self.sock.close()
        self.sock = None

    def send(self, cmd):
        self.sock.send(cmd)

    def recv(self, n_byte):
        rsp = self.sock.recv(n_byte)
        return rsp

    def transferer(self, cmd, n_byte):
        self.sock.send(cmd)
        rsp = self.sock.recv(n_byte)
        return rsp

def serveur(port):
    srv = SocketTcp()
    srv.serveur(port)
    fin = False
    lst = []
    while fin != True:
        buffer = srv.recv(100)
        print('reception message socket cliente')
        srv.send(buffer)
    srv.disconnect()

def client(adresse, port):
    clnt = SocketTcp()
    clnt.connect(adresse, port)
    clnt.send(b'hello world')
    print(clnt.recv(100))
    clnt.disconnect()
