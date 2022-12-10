from busi2c import BusI2C

class MuxI2C(BusI2C):

    def __init__(self, voie, pca9548a):
        super().__init__()
        self.canal = voie
        self.multiplexeur = pca9548a

    def scan(self):
        etat = self.multiplexeur.getCanal()
        self.multiplexeur.setCanal((1 << self.canal) | etat)
        scan = self.muliplexeur.busi2c.scan()
        self.multiplexeur.setCanal(etat)
        return scan
        
    def send(self, addr, cmd):
        etat = self.multiplexeur.getCanal()
        self.multiplexeur.setCanal((1 << self.canal) | etat)
        self.muliplexeur.busi2c.send(addr, cmd)
        self.multiplexeur.setCanal(etat)
    
    def recv(self, addr, n_byte):
        etat = self.multiplexeur.getCanal()
        self.multiplexeur.setCanal((1 << self.canal) | etat)
        data = self.muliplexeur.busi2c.recv(addr, n_byte)
        self.multiplexeur.setCanal(etat)
        return data
    
    def transferer(self, addr, cmd, n_byte):
        etat = self.multiplexeur.getCanal()
        self.multiplexeur.setCanal((1 << self.canal) | etat)
        data = self.muliplexeur.busi2c.transferer(addr, cmd, n_byte)
        self.multiplexeur.setCanal(etat)
        return data
