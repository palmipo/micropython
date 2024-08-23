class I2CBus:
    
    def scan(self):
        raise NotImplementedError
        
    def send(self, addr, cmd):
        raise NotImplementedError
    
    def recv(self, addr, n_byte):
        raise NotImplementedError
    
    def transferer(self, addr, cmd, n_byte):
        raise NotImplementedError
