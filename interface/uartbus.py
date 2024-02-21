class UartBus:
        
    def send(self, cmd):
        raise NotImplementedError
    
    def recv(self, n_byte):
        raise NotImplementedError
    
    def transfert(self, cmd, n_byte):
        raise NotImplementedError
