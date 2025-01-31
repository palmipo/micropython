import socket, struct

class Elexol:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def connect(self, address):
        addr = socket.getaddrinfo(address, 2424)[0][-1]
        self.sock.connect(addr)

    def disconnect(self):
        self.sock.close()

    def writePort(self, port, valeur):
        cmd = struct.pack('!BB', 0x41 + (port & 0x03), valeur)
        self.sock.send(cmd)

    def readPort(self, port):
        cmd = struct.pack('!B', 0x61 + (port & 0x03))
        self.sock.send(cmd)
        return struct.unpack('!BB', self.sock.recv(2))[1]

    def setDirectionPort(self, port, direction):
        cmd = b'\x21' + struct.pack('!BB', 0x41 + (port & 0x03), direction)
        self.sock.send(cmd)

    def getDirectionPort(self, port):
        cmd = b'\x21' + struct.pack('!B', 0x61 + (port & 0x03))
        self.sock.send(cmd)
        return struct.unpack('!BBB', self.sock.recv(3))[2]

    def setPullUpPort(self, port, value):
        cmd = b'\x40' + struct.pack('!BB', 0x41 + (port & 0x03), value)
        self.sock.send(cmd)

    def getPullUpPort(self, port):
        cmd = b'\x40' + struct.pack('!B', 0x61 + (port & 0x03))
        self.sock.send(cmd)
        return struct.unpack('!BH', self.sock.recv(3))[1]

    def setThreasholdPort(self, port, value):
        cmd = b'\x23' + struct.pack('!BB', (port & 0x03), value)
        self.sock.send(cmd)

    def getThreasholdPort(self, port):
        cmd = b'\x23' + struct.pack('!B', (port & 0x03))
        self.sock.send(cmd)
        return struct.unpack('!BH', self.sock.recv(3))[1]

    def setSchmittPort(self, port, value):
        cmd = b'\x24' + struct.pack('!BB', (port & 0x03), value)
        self.sock.send(cmd)

    def getSchmittPort(self, port):
        cmd = b'\x24' + struct.pack('!B', (port & 0x03))
        self.sock.send(cmd)
        return struct.unpack('!BH', self.sock.recv(3))[1]

# control bit EEPROM
# The Control Bits 1 Location is used to turn on and off the Fixed IP address, Preset Port and AutoScan 
# mode functions. When the EEPROM is blank it reads all ones i.e. each blank word reads 65535 ro 
# $FFFF. Because of this we use a 0 bit value to turn a function on.
# The currently used bits are bit 0, which is used to enable the Fixed IP address,
# Bit 1, which is used to enable the Preset Port function and 
# Bit 2, which is used to enable the AutoScan function.
# All the remaining bits should be left as ones for future compatibility as the firmware is upgraded
# and additional functions adde
    def readEepromWord(self, address):
        cmd = b'\x27\x52' + struct.pack('!B', address) + b'\x00\x00'
        self.sock.send(cmd)
        rsp = self.sock.recv(4)
        return int.from_bytes(rsp[2:4], byteorder='big', signed=False)

    def writeEepromWord(self, address, value):
        cmd = b'\x27\x57' + struct.pack('!BH', address, value)
        self.sock.send(cmd)

    def eraseEepromWord(self, address):
        cmd = b'\x27\x45' + struct.pack('!B', address) + b'\xAA\x55'
        self.sock.send(cmd)

    def writeEnableEeprom(self):
        cmd = b'\x27\0x31\x00\xAA\x55'
        self.sock.send(cmd)

    def writeDisableEeprom(self):
        cmd = b'\x27\0x30\x00\x00\x00'
        self.sock.send(cmd)

    def echo(self, data):
        cmd = b'\x2A' + struct.pack('!B', data)
        self.sock.send(cmd)
        return struct.unpack('!BB', self.sock.recv(2))[1]

    def resetModule(self):
        cmd = b'\x27\x40\x00\xAA\x55'
        self.sock.send(cmd)
    
    def identifyIO24Units(self):
        cmd = b'\x49\x4F\x32\x34'
        self.sock.send(cmd)
        data = struct.unpack('!BBBBBBBBBBH', self.sock.recv(12))
        mac = '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(data[4], data[5], data[6], data[7], data[8], data[9])
        firmware = data[10]
        return (mac, firmware)
    
    def sendHostData(self):
        cmd = b'\x25'
        self.sock.send(cmd)
        data = struct.unpack('!BBBBBBBBBBBBBBH', self.sock.recv(16))
        print(data)
        serial = '{:03}.{:03}.{:03}'.format(data[1], data[2], data[3])
        ip = '{:03}.{:03}.{:03}.{:03}'.format(data[4], data[5], data[6], data[7])
        mac = '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(data[8], data[9], data[10], data[11], data[12], data[13])
        port = data[14]
        return serial, ip, mac, port

if __name__ == "__main__":
    from tools.configfile import ConfigFile
    cfg = ConfigFile('master/net/wifi.json')
    from master.net.wlanpico import WLanPico
    wlan = WLanPico()
    try:
        wlan.connect(cfg.config()['wifi']['ssid'], cfg.config()['wifi']['passwd'])
        print(wlan.ifconfig())
        elexol = Elexol()
        elexol.connect("192.168.1.120")
        print(elexol.identifyIO24Units())
        print(elexol.sendHostData())
        elexol.disconnect()
    finally:
        wlan.disconnect()
