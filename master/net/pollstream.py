import socket
from interface.socketbus import SocketBus

class PollStream:
    def __init__(self, sock_srv=None):
        self.poule = select.poll()
        self.sock_srv = sock_srv
        
        if self.sock_srv != None:
            self.poule.register(self.sock_srv, select.POLLIN | select.POLLERR | select.POLLHUP)
    
    def scrute(self, timeout):
        events = self.poule.poll(timeout)

        for (fd, event) in events:
            if (event == select.POLLIN):
                if fd == self.sock_srv:
                    s = fd.accept()
                    s.setblocking(True)
                    self.poule.register(s, select.POLLIN | select.POLLERR | select.POLLHUP)
                    return 0, s
                else:
                    return 1, fd
            else:
                fd.disconnect()
                return -1, fd

    def connect(self, adresse, port):
        self.sock_srv.connect(socket.getaddrinfo(adresse, port)[0][-1])

    def disconnect(self):
        if self.mode == self.SERVEUR:
            self.poule.unregister(self.sock_srv)
        self.sock_srv.close()
        self.sock_srv = None

    def send(self, cmd):
        self.sock_srv.send(cmd)

    def recv(self, n_byte):
        rsp = self.sock_srv.recv(n_byte)
        return rsp

    def transferer(self, cmd, n_byte):
        self.sock_srv.send(cmd)
        rsp = self.self.sock_srv(n_byte)
        return rsp

def serveur(port):
    srv = SocketTcp()
    srv.serveur(port)
    
    poule = PollStream(srv)

    fin = False
    lst = []
    while fin != True:
        etat, fd = poule.scrute(10000)

        # erreur socket
        if etat < 0:
            print('erreur socket')
            for c in lst:
                if c.sock == fd:
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
