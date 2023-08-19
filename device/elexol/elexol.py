import socket

class Elexol:
    def __init__(self, address):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.connect(socket.getaddrinfo(address, 2424)[0][-1])

    def deconnexion(self):
        self.__socket.close()

    def writePort(self, port, valeur):
        cmd = bytearray(2)
        cmd[0] = 0x41 + (port & 0x03)
        cmd[1] = valeur & 0xFF
        self.__socket.send(cmd)

    def readPort(self, port):
        cmd = bytearray(1)
        cmd[0] = 0x61 + (port & 0x03)
        self.__socket.send(cmd)
        rsp = self.__socket.recv(2)
        return rsp[1]

    def setDirectionPort(self, port, direction):
        cmd = bytearray(3)
        cmd[0] = 0x21
        cmd[1] = 0x41 + (port & 0x03)
        cmd[2] = direction & 0xFF
        self.__socket.send(cmd)

    def getDirectionPort(self, port):
        cmd = bytearray(2)
        cmd[0] = 0x21
        cmd[1] = 0x61 + (port & 0x03)
        self.__socket.send(cmd)
        rsp = self.__socket.recv(3)
        return rsp[2]

    def setPullUpPort(self, port, value):
        cmd = bytearray(3)
        cmd[0] = 0x40
        cmd[1] = 0x41 + (port & 0x03)
        cmd[2] = value & 0xFF
        self.__socket.send(cmd)

    def setThreasholdPort(self, port, value):
        cmd = bytearray(3)
        cmd[0] = 0x23
        cmd[1] = 0x41 + (port & 0x03)
        cmd[2] = value & 0xFF
        self.__socket.send(cmd)

    def setSchmittPort(self, port, value):
        cmd = bytearray(3)
        cmd[0] = 0x24
        cmd[1] = 0x41 + (port & 0x03)
        cmd[2] = value & 0xFF
        self.__socket.send(cmd)
    
    def identifyIO24Units(self):
        cmd = b'\x49\x4F\x32\x34'
        self.__socket.send(cmd)
        rsp = self.__socket.recv(12)
        mac = rsp[4:10]
        firmware = rsp[10:12]
        return mac, firmware

    def readEepromWord(self, address):
        cmd = bytearray(3)
        cmd[0] = 0x27
        cmd[1] = 0x52
        cmd[2] = address & 0xFF
        self.__socket.send(cmd)
        rsp = self.__socket.recv(4)
        return int.from_bytes(rsp[2:4], byteorder='big', signed=False)

    def writeEepromWord(self, address, value):
        val = value.to_bytes(length=2, byteorder='big', signed=False)
        cmd = bytearray(5)
        cmd[0] = 0x27
        cmd[1] = 0x57
        cmd[2] = address & 0xFF
        cmd[3] = val[0]
        cmd[4] = val[1]
        self.__socket.send(cmd)

    def eraseEepromWord(self, address):
        cmd = bytearray(5)
        cmd[0] = 0x27
        cmd[1] = 0x45
        cmd[2] = address & 0xFF
        cmd[3] = 0xAA
        cmd[4] = 0x55
        self.__socket.send(cmd)

    def writeEnableEeprom(self):
        cmd = b'\x27\0x31\x00\xAA\x55'
        self.__socket.send(cmd)

    def writeDisableEeprom(self):
        cmd = b'\x27\0x30\x00\x00\x00'
        self.__socket.send(cmd)

    def resetModule(self):
        cmd = b'\x27\x52\x00\xAA\x55'
        self.__socket.send(cmd)

