import time, struct, select

class Pico_eth_ch9121:
    def __init__(self, cfg, reset, uart0, uart1=None):
        self.TIMEOUT = 100
        self.uart = [uart0, uart1]
        self.CFG = cfg
        self.RST = reset
        self.CFG.value(1)
        self.RST.value(1)
        self.poule = select.poll()
        self.poule.register(self.uart[0], select.POLLIN | select.POLLERR | select.POLLHUP)
        if uart1 != None:
            self.poule.register(self.uart[1], select.POLLIN | select.POLLERR | select.POLLHUP)

    def config(self, dhcp=1, ip="192.168.1.3", mask="255.255.255.0", gateway="192.168.1.1", random_port0=1, port0=2000, random_port1=1, port1=2000):
        self.CFG.value(0)
        time.sleep(1)
        
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

        self.CFG.value(1)
        time.sleep(1)


    def connect(self, port, mode, ip, port_number):
        self.CFG.value(0)
        time.sleep(1)

        self.setDeviceMode(port, mode)
        self.setDestinationIpAddress(port, ip)
        self.setDestinationPortNumber(port, port_number)

        self.CFG.value(1)
        time.sleep(1)

    def reset(self):
        self.uart[0].write(b'\x57\xab\x02')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)
        raise Exception

    def saveParametters(self):
        self.uart[0].write(b'\x57\xab\x0d')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def restoreParametters(self):
        self.uart[0].write(b'\x57\xab\x0e')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceDhcp(self, turn_on):
        self.uart[0].write(b'\x57\xab\x33'+ struct.pack('<B', turn_on))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDomainName(self, domaine_name):
#         self.self.uart[0].write(b'\x57\xab\x34'+ struct.pack('<s', c for c in domaine_name:))
#                 events = self.poule.poll(self.TIMEOUT)
#         for (fd, event) in events:
#             if (event == select.POLLIN):

#         return self.self.uart[0].read(1) == 0xaa
        pass

    def turnOnPort2(self, turn_on):
        self.uart[0].write(b'\x57\xab\x39'+ struct.pack('<B', turn_on))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceMode(self, port, mode):
        p = 0x10
        if port == 1:
            p = 0x40
        self.uart[0].write(b'\x57\xab'+ struct.pack('<BB', p, mode%4))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceIpAddress(self, ip):
        self.uart[0].write(b'\x57\xab\x11'+ bytes(map(int, ip.split('.'))))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceSubnetMask(self, ip):
        self.uart[0].write(b'\x57\xab\x12'+ bytes(map(int, ip.split('.'))))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceGatewayAddress(self, ip):
        self.uart[0].write(b'\x57\xab\x13'+ bytes(map(int, ip.split('.'))))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDevicePortNumber(self, port, random, num_port):
        p = 0x17
        if port == 1:
            p = 0x47
        self.uart[0].write(b'\x57\xab\x17' + struct.pack('<B', p) + struct.pack('<B', random))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

        p = 0x14
        if port == 1:
            p = 0x41
        self.uart[0].write(b'\x57\xab'+ struct.pack('<BH', p, num_port))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceBaudRate(self, port, baud_rate, data_bit, parity, stop):
        p = 0x21
        if port == 1:
            p = 0x44
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p) + struct.pack('<I', baud_rate))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

        p = 0x22
        if port == 1:
            p = 0x45
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p) + struct.pack('<BBB', stop%1, parity%5, data_bit%9))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceTimeout(self, port, timeout):
        p = 0x23
        if port == 1:
            p = 0x46
        self.uart[0].write(b'\x57\xab'+ struct.pack('<BI', p, timeout))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceNetworkCableDisconnection(self, disconnection):
        self.uart[0].write(b'\x57\xab\x24'+ struct.pack('<B', disconnection%2))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceReceivingPacketLength(self, port, packet_length):
        p = 0x25
        if port == 1:
            p = 0x48
        self.uart[0].write(b'\x57\xab' + struct.pack('<BI', p, packet_length))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDestinationIpAddress(self, port, ip):
        p = 0x15
        if port == 1:
            p = 0x42
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p) + bytes(map(int, ip.split('.'))))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDestinationPortNumber(self, port, port_number):
        p = 0x16
        if port == 1:
            p = 0x43
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p) + struct.pack('<H', port_number))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setCleanOnConnection(self, port, disconnect):
        p = 0x26
        if port == 1:
            p = 0x49
        self.uart[0].write(b'\x57\xab'+ struct.pack('<BB', p, disconnect))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def getChipVersionNumber(self):
        self.uart[0].write(b'\x57\xab\x01')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return fd.read(1).hex()

    def getConnectionStatus(self, port):
        p = 0x03
        if port == 1:
            p = 0x04
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return fd.read()

    def getDeviceMode(self, port):
        p = 0x60
        if port == 1:
            p = 0x90
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return fd.read()
        raise Exception

    def getDeviceIpAddress(self):
        self.uart[0].write(b'\x57\xab\x61')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                ip = struct.unpack('<BBBB', fd.read(4))
                return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])
        raise Exception

    def getDeviceMaskSubnet(self):
        self.uart[0].write(b'\x57\xab\x62')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                ip = struct.unpack('<BBBB', fd.read(4))
                return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])
        raise Exception

    def getDeviceGateway(self):
        self.uart[0].write(b'\x57\xab\x63')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                ip = struct.unpack('<BBBB', fd.read(4))
                return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])
        raise Exception

    def getDevicePort(self, port):
        p = 0x64
        if port == 1:
            p = 0x91
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return struct.unpack('<H', fd.read(2))[0]
        raise Exception

    def getDeviceBaudRate(self, port):
        baud_rate=0
        data_bit=0
        parity=0
        stop=0
        p = 0x71
        if port == 1:
            p = 0x94
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                baud_rate = struct.unpack('<I', fd.read(4))[0]

        p = 0x72
        if port == 1:
            p = 0x95
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                data = struct.unpack('<BBB', fd.read(3))
                stop = data[0]
                parity = data[1]
                data_bit = data[2]

        return baud_rate, data_bit, parity, stop

    def getDestinationIpAddress(self, port):
        p = 0x65
        if port == 1:
            p = 0x92
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                ip = struct.unpack('<BBBB', fd.read(4))
                return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])
        raise Exception

    def getDestinationTimeout(self, port):
        p = 0x73
        if port == 1:
            p = 0x96
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return self.fd.read()
        raise Exception

    def getDestinationPort(self, port):
        p = 0x66
        if port == 1:
            p = 0x93
        self.uart[0].write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return struct.unpack('<H', fd.read(2))
        raise Exception

    def getDeviceMacAddress(self):
        self.uart[0].write(b'\x57\xab\x81')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                mac = struct.unpack('<BBBBBB', fd.read(6))
                return '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])
        raise Exception

if __name__ == "__main__":
    import machine
    uart0 = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))
    uart0.init(baudrate=9600, bits=8, parity=None, stop=1)
    uart1 = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))
    uart1.init(baudrate=9600, bits=8, parity=None, stop=1)
    CFG = machine.Pin(14, machine.Pin.OUT)
    CFG.value(1)
    RST = machine.Pin(17, machine.Pin.OUT)
    RST.value(1)
    
    eth = Pico_eth_ch9121(CFG, RST, uart0, uart1)
    eth.config()

    CFG.value(0)
    time.sleep(0.1)
    print(eth.getDeviceMode(0), eth.getDeviceMode(1))
    print(eth.getDeviceIpAddress())
    print(eth.getDeviceMaskSubnet())
    print(eth.getDeviceGateway())
    print(eth.getDevicePort(0), eth.getDevicePort(1))
    CFG.value(1)

    eth.connect(0, 1, '162.159.200.123', 123)

    CFG.value(0)
    time.sleep(0.1)
    eth.getConnectionStatus(0)
    print(eth.getDeviceMacAddress())
    CFG.value(1)
