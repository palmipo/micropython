from interface.i2cbus import I2CBus

class I2CMux(I2CBus):

    def __init__(self, voie, pca9548a):#, i2c):
        super().__init__()
        self.__canal__ = voie
        self.__multiplexeur__ = pca9548a
        self.__multiplexeur__.clear()

    def scan(self):
        self.__multiplexeur__.setCanal(1 << self.__canal__)
        res = self.__multiplexeur__.busi2c.scan()
        return res
        
    def send(self, addr, cmd):
        self.__multiplexeur__.setCanal(1 << self.__canal__)
        self.__multiplexeur__.busi2c.send(addr, cmd)
    
    def recv(self, addr, n_byte):
        self.__multiplexeur__.setCanal(1 << self.__canal__)
        data = self.__multiplexeur__.busi2c.recv(addr, n_byte)
        return data
    
    def transferer(self, addr, cmd, n_byte):
        self.__multiplexeur__.setCanal(1 << self.__canal__)
        data = self.__multiplexeur__.busi2c.transferer(addr, cmd, n_byte)
        return data
