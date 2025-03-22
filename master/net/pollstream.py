import socket, select
from interface.socketbus import SocketBus

class PollStream:
    def __init__(self):
        self.poule = select.poll()
        self.lst = []
    
    def register(self, flux):
        self.poule.register(flux, select.POLLIN | select.POLLERR | select.POLLHUP)
        self.lst.append(flux)

    def unregister(self, flux):
        self.poule.unregister(flux)
        self.lst.remove(flux)
    
    def scrute(self, timeout):
        events = self.poule.poll(timeout)
        for (fd, event) in events:
            if event == select.POLLIN:
                return 1, fd
            
            elif event == select.POLLERR or event == select.POLLHUP:
                return -1, fd

            else:
                return 0, None
# 
# if __name__ == "__main__":
#     def serveur(port):
#         srv = SocketTcp()
#         srv.serveur(port)
#         
#         poule = PollStream()
#         poule.register(srv)
# 
#         fin = False
#         lst = []
#         while fin != True:
#             etat, fd = poule.scrute(10000)
# 
#             # erreur socket
#             if etat < 0:
#                 print('erreur socket')
#                 poule.unregister(fd)
#                 fin = True
# 
#             # reception sur une socket cliente
#             elif etat > 0:
#                 if fd == srv.sock:
#                     lst.append(SocketTcp(srv.accept()[0]))
#                 
#                 else:
#                     print('reception message socket cliente')
#                     buffer = fd.recv(100)
#                     fd.send(buffer)
# 
#             else:
#                 print('timeout')
# 
#     def client(adresse, port):
#         clnt = SocketTcp()
#         clnt.connect(adresse, port)
#         clnt.send(b'hello world')
#         etat, fd = clnt.scrute(10000)
#         if etat == 1:
#             print(fd.recv(100))
#         clnt.disconnect()
# 
