import time, struct, select
from micropython import const

class Pico_eth_ch9121:
    def __init__(self, cfg, reset, uart0, uart1=None):
        self.TIMEOUT = const(100)
        self.CFG_TEMPO = const(10)
        self.RST_TEMPO = const(10)
        self.TCP_SERVER = const(0)
        self.TCP_CLIENT = const(1)
        self.UDP_SERVER = const(2)
        self.UDP_CLIENT = const(3)

        self.uart = [uart0, uart1]
        self.CFG = cfg
        self.RST = reset
        self.CFG.value(1)
        self.RST.value(1)
        self.poule = select.poll()
        self.poule.register(self.uart[0], select.POLLIN | select.POLLERR | select.POLLHUP)
        if uart1 != None:
            self.poule.register(self.uart[1], select.POLLIN | select.POLLERR | select.POLLHUP)

    def setConfigMode(self):
        self.CFG.value(0)
        time.sleep_ms(self.CFG_TEMPO)

    def setDataMode(self):
        self.CFG.value(1)
        time.sleep_ms(self.CFG_TEMPO)
    
    def config(self, dhcp=1, ip="192.168.1.3", mask="255.255.255.0", gateway="192.168.1.1", random_port0=1, port0=2000, random_port1=1, port1=2000):
        self.setDeviceDhcp(dhcp)
        if dhcp == 0:
            self.setDeviceIpAddress(ip)
            self.setDeviceSubnetMask(mask)
            self.setDeviceGatewayAddress(gateway)

        self.setDevicePortNumber(0, random_port0, port0)

        if self.uart[1] == None:
            self.turnOnPort2(0)
        else:
            self.turnOnPort2(1)
            self.setDevicePortNumber(1, random_port1, port1)

        self.saveParametters()
        self.restoreParametters()

    def connect(self, port, mode, ip, port_number):
        self.setConfigMode()

        self.setDeviceMode(port, mode)
        self.setDestinationIpAddress(port, ip)
        self.setDestinationPortNumber(port, port_number)

        self.saveParametters()
        self.restoreParametters()

        self.setDataMode()

    def reset(self):
        self.RST.value(0)
        time.sleep_ms(self.RST_TEMPO)

        self.RST.value(1)
        time.sleep_ms(self.RST_TEMPO)

        self.setConfigMode()

        self.__send__(b'\x57\xab\x02', b'\xaa')

        self.setDataMode()

    def saveParametters(self):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x0d', b'\xaa')

        self.setDataMode()

    def restoreParametters(self):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x0e', b'\xaa')

        self.setDataMode()

    def setDeviceDhcp(self, turn_on):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x33'+ struct.pack('<B', turn_on), b'\xaa')

        self.setDataMode()

    def setDomainName(self, domaine_name):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x34'+ domaine_name, b'\xaa')

        self.setDataMode()

    def turnOnPort2(self, turn_on):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x39'+ struct.pack('<B', turn_on), b'\xaa')

        self.setDataMode()

    # 00: TCP server
    # 01: TCP client
    # 02: UDP server
    # 03: UDP client
    def setDeviceMode(self, port, mode):
        self.setConfigMode()

        p = 0x10
        if port == 1:
            p = 0x40
        self.__send__(b'\x57\xab'+ struct.pack('<BB', p, mode%4), b'\xaa')

        self.setDataMode()

    def setDeviceIpAddress(self, ip):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x11'+ bytes(map(int, ip.split('.'))), b'\xaa')

        self.setDataMode()

    def setDeviceSubnetMask(self, ip):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x12'+ bytes(map(int, ip.split('.'))), b'\xaa')

        self.setDataMode()

    def setDeviceGatewayAddress(self, ip):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x13'+ bytes(map(int, ip.split('.'))), b'\xaa')

        self.setDataMode()

    def setDevicePortNumber(self, port, random, num_port):
        self.setConfigMode()

        p = 0x17
        if port == 1:
            p = 0x47
        self.__send__(b'\x57\xab\x17' + struct.pack('<B', p) + struct.pack('<B', random), b'\xaa')

        p = 0x14
        if port == 1:
            p = 0x41
        self.__send__(b'\x57\xab'+ struct.pack('<BH', p, num_port), b'\xaa')

        self.setDataMode()

    def setDeviceBaudRate(self, port, baud_rate, data_bit, parity, stop):
        self.setConfigMode()

        p = 0x21
        if port == 1:
            p = 0x44
        self.__send__(b'\x57\xab' + struct.pack('<B', p) + struct.pack('<I', baud_rate), b'\xaa')

        p = 0x22
        if port == 1:
            p = 0x45
        self.__send__(b'\x57\xab' + struct.pack('<B', p) + struct.pack('<BBB', stop%1, parity%5, data_bit%9), b'\xaa')

        self.setDataMode()

    def setDeviceTimeout(self, port, timeout):
        self.setConfigMode()

        p = 0x23
        if port == 1:
            p = 0x46
        self.__send__(b'\x57\xab'+ struct.pack('<BI', p, timeout), b'\xaa')

        self.setDataMode()

    def setDeviceNetworkCableDisconnection(self, disconnection):
        self.setConfigMode()

        self.__send__(b'\x57\xab\x24'+ struct.pack('<B', disconnection%2), b'\xaa')

        self.setDataMode()

    def setDeviceReceivingPacketLength(self, port, packet_length):
        self.setConfigMode()

        p = 0x25
        if port == 1:
            p = 0x48
        self.__send__(b'\x57\xab' + struct.pack('<BI', p, packet_length), b'\xaa')

        self.setDataMode()

    def setDestinationIpAddress(self, port, ip):
        self.setConfigMode()

        p = 0x15
        if port == 1:
            p = 0x42
        self.__send__(b'\x57\xab' + struct.pack('<B', p) + bytes(map(int, ip.split('.'))), b'\xaa')

        self.setDataMode()

    def setDestinationPortNumber(self, port, port_number):
        self.setConfigMode()

        p = 0x16
        if port == 1:
            p = 0x43
        self.__send__(b'\x57\xab' + struct.pack('<B', p) + struct.pack('<H', port_number), b'\xaa')

        self.setDataMode()

    def setCleanOnConnection(self, port, disconnect):
        self.setConfigMode()

        p = 0x26
        if port == 1:
            p = 0x49
        self.__send__(b'\x57\xab'+ struct.pack('<BB', p, disconnect), b'\xaa')

        self.setDataMode()

    def __send__(self, data, res):
        self.uart[0].write(data)
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                c = fd.read(1)
                if c:
                    assert c == res

    def __recv__(self, msg, length):
        self.setConfigMode()

        data = bytes()
        self.uart[0].write(msg)
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                data = fd.read(length)

        self.setDataMode()
        
        return data

    def getChipVersionNumber(self):
        return self.__recv__(b'\x57\xab\x01', 1)

    def getConnectionStatus(self, port):
        p = 0x03
        if port == 1:
            p = 0x04
        return self.__recv__(b'\x57\xab' + struct.pack('<B', p), 1)

    def getDeviceMode(self, port):
        mode = 0
        p = 0x60
        if port == 1:
            p = 0x90
        return self.__recv__(b'\x57\xab' + struct.pack('<B', p), 1)

    def getDeviceIpAddress(self):
        data = self.__recv__(b'\x57\xab\x61', 4)
        ip = '{:03}.{:03}.{:03}.{:03}'.format(data[0], data[1], data[2], data[3])
        return ip

    def getDeviceMaskSubnet(self):
        data = self.__recv__(b'\x57\xab\x62', 4)
        ip = '{:03}.{:03}.{:03}.{:03}'.format(data[0], data[1], data[2], data[3])
        return ip

    def getDeviceGateway(self):
        data = self.__recv__(b'\x57\xab\x63', 4)
        ip = '{:03}.{:03}.{:03}.{:03}'.format(data[0], data[1], data[2], data[3])
        return ip

    def getDevicePort(self, port):
        p = 0x64
        if port == 1:
            p = 0x91
        data = self.__recv__(b'\x57\xab' + struct.pack('<B', p), 2)
        return struct.unpack('<H', data)[0]

    def getDeviceBaudRate(self, port):
        baud_rate=0
        data_bit=0
        parity=0
        stop=0
        p = 0x71
        if port == 1:
            p = 0x94
        data = self.__recv__(b'\x57\xab' + struct.pack('<B', p), 4)
        baud_rate = struct.unpack('<I', data)[0]

        p = 0x72
        if port == 1:
            p = 0x95
        res = self.__recv__(b'\x57\xab' + struct.pack('<B', p), 3)
        data = struct.unpack('<BBB', res)
        stop = data[0]
        parity = data[1]
        data_bit = data[2]

        return baud_rate, data_bit, parity, stop

    def getDestinationIpAddress(self, port):
        p = 0x65
        if port == 1:
            p = 0x92
        data = self.__recv__(b'\x57\xab' + struct.pack('<B', p), 4)
        ip = struct.unpack('<BBBB', data)
        return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])

    def getDestinationTimeout(self, port):
        p = 0x73
        if port == 1:
            p = 0x96
        data = self.__recv__(b'\x57\xab' + struct.pack('<B', p), 1)
        return data

    def getDestinationPort(self, port):
        p = 0x66
        if port == 1:
            p = 0x93
        data = self.__recv__(b'\x57\xab' + struct.pack('<B', p), 2)
        return struct.unpack('<H', data)

    def getDeviceMacAddress(self):
        data = self.__recv__(b'\x57\xab\x81', 6)
        mac = struct.unpack('<BBBBBB', data)
        return '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])

    def write(self, port, data):
        self.uart[port].write(data)
    
    def read(self, port, length=0):
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return fd.read(length)

if __name__ == "__main__":
    import machine
    uart0 = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1), timeout=5000)
    uart0.init(baudrate=9600, bits=8, parity=None, stop=1)
    uart1 = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5), timeout=5000)
    uart1.init(baudrate=9600, bits=8, parity=None, stop=1)
    CFG = machine.Pin(14, machine.Pin.OUT)
    RST = machine.Pin(17, machine.Pin.OUT)
    
    eth = Pico_eth_ch9121(CFG, RST, uart0, uart1)
    eth.reset()
    eth.config()

    print(eth.getDeviceMode(0), eth.getDeviceMode(1))
    print(eth.getDeviceIpAddress())
    print(eth.getDeviceMaskSubnet())
    print(eth.getDeviceGateway())
    print(eth.getDevicePort(0), eth.getDevicePort(1))

    eth.connect(0, eth.TCP_CLIENT, '192.168.1.108', 1883)
    eth.write(0, b'\x10\x2d\x00\x04MQTT\x04\xc2\x00\x00\x00\x10e6614c311b32b728\x00\x04toff\x00\x0acrapaud8))')
    print(eth.read(1))
    eth.write(0, b'\xE0\x00')

    print(eth.getConnectionStatus(0))
    print(eth.getDeviceMacAddress())
    
    eth.setCleanOnConnection(0, 1)
