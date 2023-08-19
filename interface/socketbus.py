class SocketBus:

    def connexion(self, adresse, port):
        raise NotImplementedError

    def deconnexion(self):
        raise NotImplementedError

    def send(self, cmd):
        raise NotImplementedError
    
    def recv(self, n_byte):
        raise NotImplementedError
    
    def transfer(self, cmd, n_byte):
        raise NotImplementedError
