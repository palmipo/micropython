class BusSerial:
        
    def send(self, cmd):
        raise NotImplementedError
    
    def recv(self, n_byte):
        raise NotImplementedError
    
    def transferer(self, cmd, n_byte):
        raise NotImplementedError
