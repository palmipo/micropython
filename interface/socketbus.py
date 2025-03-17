class SocketBus:
    def __init__(self):
        self.SERVEUR = 1
        self.CLIENT = 2
        self.mode = self.CLIENT

    def serveur(self, port):
        raise NotImplementedError
    
    def client(self, adresse, port):
        raise NotImplementedError

    def connect(self, adresse, port):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def send(self, cmd):
        raise NotImplementedError
    
    def recv(self, n_byte):
        raise NotImplementedError
    
    def transferer(self, cmd, n_byte):
        raise NotImplementedError
