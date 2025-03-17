import socket
from interface.socketbus import SocketBus

class SocketTcp(SocketBus):
    def __init__(self, sock=None):
        super.__init__()

        if sock == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setblocking(True)
            self.poule = select.poll()
            self.poule.register(self.sock, select.POLLIN | select.POLLERR | select.POLLHUP)

        else:
            self.sock = sock
            self.sock.setblocking(True)
            self.poule = None

    def serveur(self, port):
        self.mode = self.SERVEUR
        self.sock.bind(port)
        self.sock.listen()
    
    def scrute(self, timeout):
        events = self.poule.poll(timeout)

        for (fd, event) in events:
            if (event == select.POLLIN):
                if fd == self.sock:
                    if self.mode == self.SERVEUR:
                        s = self.sock.accept()
                        s.setblocking(True)
                        self.poule.register(s, select.POLLIN | select.POLLERR | select.POLLHUP)
                        return 0, s
                    else:
                        return 1, fd
                else:
                    return 1, fd
            else:
                if fd == self.sock:
                    self.disconnect()
                    return -1, fd

                else:
                    self.poule.unregister(fd)
                    fd.close()
                    return -2, fd

    def connect(self, adresse, port):
        self.sock.connect(socket.getaddrinfo(adresse, port)[0][-1])

    def disconnect(self):
        if self.mode == self.SERVEUR:
            self.poule.unregister(self.sock)
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
        etat, fd = srv.scrute(10000)

        # erreur socket cliente
        if etat == -2:
            print('erreur socket cliente')
            for c in lst:
                if c.sock == fd:
                    lst.remove(c)

        # erreur socket ecoute
        elif etat == -1:
            print('erreur socket ecoute')
            for c in lst:
                c.disconnect()
                lst.remove(c)
            fin = True

        # reception sur une socket cliente
        elif etat == 1:
            print('reception message socket cliente')
            buffer = fd.recv(100)
            fd.send(buffer)

        else:
            print('connexion d\'un nouveau client')
            lst.append(SocketTcp(fd))

def client(adresse, port):
    clnt = SocketTcp()
    clnt.connect(adresse, port)
    clnt.send(b'hello world')
    etat, fd = clnt.scrute(10000)
    if etat == 1:
        print(fd.recv(100))
    clnt.disconnect()
