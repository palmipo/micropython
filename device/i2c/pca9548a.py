from devicei2c import DeviceI2C
import machine
import time

class PCA9548A(DeviceI2C):

    def __init__(self, address, bus, reset_pin=0):
        super().__init__(0x70 | (address & 0x03), bus)
        if reset_pin != 0:
            self.__reset__ = machine.Pin(reset_pin, machine.Pin.OUT)
            self.__reset__.on()

    def reset(self):
        self.__reset__.off()
        time.sleep_ms(1)
        self.__reset__.on()
        time.sleep_ms(100)

    def clear(self):
        cmd = bytearray(1)
        cmd[0] = 0
        self.busi2c.send(self.adresse, cmd)

    def setCanal(self, canal):
        cmd = bytearray(1)
        cmd[0] = canal & 0xff
        self.busi2c.send(self.adresse, cmd)

    def getCanal(self):
        return self.busi2c.recv(self.adresse, 1)[0]

            
if __name__=='__main__':
    i2c = PicoI2C(0, 4, 5)
    print("liste des circuits i2c presents sur le bus :")
    print(i2c.scan())

    pca9548a = PCA9548A(0, i2c, 3)
    pca9548a.reset()
    for i in range(0, 8):
        pca9548a.setCanal(i)
        print("liste des circuits i2c presents sur le bus :")
        print(i2c.scan())
