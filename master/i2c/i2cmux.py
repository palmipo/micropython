from i2cbus import I2CBus

class I2CMux(I2CBus):

    def __init__(self, voie, pca9548a, i2c):
        super().__init__()
        self.__canal = voie
        self.__multiplexeur = pca9548a
        self.__multiplexeur.clear()
        self.__busi2c = i2c

    def scan(self):
        self.__multiplexeur.setCanal(1 << self.__canal)
        res = self.__busi2c.scan()
        return res
        
    def send(self, addr, cmd):
        self.__multiplexeur.setCanal(1 << self.__canal)
        self.__busi2c.send(addr, cmd)
    
    def recv(self, addr, n_byte):
        self.__multiplexeur.setCanal(1 << self.__canal)
        data = self.__busi2c.recv(addr, n_byte)
        return data
    
    def transferer(self, addr, cmd, n_byte):
        self.__multiplexeur.setCanal(1 << self.__canal)
        data = self.__busi2c.transferer(addr, cmd, n_byte)
        return data
