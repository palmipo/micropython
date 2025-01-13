import time, struct, select

class Pico_eth_ch9121:
    def __init__(self, uart, cfg, reset):
        self.TIMEOUT = 100
        self.uart = uart
        self.CFG = cfg
        self.RST = reset
        self.CFG.value(1)
        self.RST.value(1)
        self.poule = select.poll()
        self.poule.register(self.uart, select.POLLIN | select.POLLERR | select.POLLHUP)

    def config(self, dhcp=1, ip="192.168.1.3", mask="255.255.255.0", gateway="192.168.1.1", randomport=1, port=2222):
        self.CFG.value(0)
        time.sleep(1)

#         self.reset()
        print(self.getChipVersionNumber())
        
        self.setDeviceDhcp(dhcp)
        if dhcp == 0:
            self.setDeviceIpAddress(ip)
            self.setDeviceSubnetMask(mask)
            self.setDeviceGatewayAddress(gateway)

        self.setDeviceRandomPortNumber(randomport)
        if randomport == 0:
            self.setDevicePortNumber(0, port)

        self.saveParametters()
        self.restoreParametters()
        
#         self.uart.write(b'\x57\xab\x5e')
#         events = self.poule.poll(self.TIMEOUT)
#         for (fd, event) in events:
#             if (event == select.POLLIN):
#                 print('live serial port configuration mode {}'.format(fd.read()))
#         assert fd.read(1) == struct.pack('<B', 0xaa)

        self.CFG.value(1)
        time.sleep(1)


    def connect(self, mode, ip, port):
        self.CFG.value(0)
        time.sleep(1)

        self.setDeviceMode(0, mode)
        self.setDestinationIpAddress(0, ip)
        self.setDestinationPortNumber(0, port)

        self.CFG.value(1)
        time.sleep(1)

    def getChipVersionNumber(self):
        self.uart.write(b'\x57\xab\x01')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return fd.read(1).hex()

    def reset(self):
        self.uart.write(b'\x57\xab\x02')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def getConnectionStatus(self, port):
        p = 3
        if port == 2:
            p = 4
        self.uart.write(b'\x57\xab' + struct.pack('<B', p))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                print(fd.read())
                return fd.read()

    def saveParametters(self):
        self.uart.write(b'\x57\xab\x0d')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def restoreParametters(self):
        self.uart.write(b'\x57\xab\x0e')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceDhcp(self, turn_on):
        self.uart.write(b'\x57\xab\x33'+ struct.pack('<B', turn_on))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDomainName(self, domaine_name):
#         self.self.uart.write(b'\x57\xab\x34'+ struct.pack('<s', c for c in domaine_name:))
#                 events = self.poule.poll(self.TIMEOUT)
#         for (fd, event) in events:
#             if (event == select.POLLIN):

#         return self.self.uart.read(1) == 0xaa
        pass

    def turnOnPort2(self, turn_on):
        self.uart.write(b'\x57\xab\x39'+ struct.pack('<B', turn_on))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)
        
    def setDeviceMode(self, port, mode):
        p = 0x10
        if port == 2:
            port = 0x40
        self.uart.write(b'\x57\xab'+ struct.pack('<BB', p, mode%4))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceIpAddress(self, ip):
        self.uart.write(b'\x57\xab\x11'+ bytes(map(int, ip.split('.'))))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceSubnetMask(self, ip):
        self.uart.write(b'\x57\xab\x12'+ bytes(map(int, ip.split('.'))))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceGatewayAddress(self, ip):
        self.uart.write(b'\x57\xab\x13'+ bytes(map(int, ip.split('.'))))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDevicePortNumber(self, port, num_port):
        p = 0x14
        if port == 2:
            port = 0x41
        self.uart.write(b'\x57\xab'+ struct.pack('<BH', p, num_port))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceRandomPortNumber(self, port):
        self.uart.write(b'\x57\xab\x17'+ struct.pack('<B', port))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceBaudRate(self, port, baud_rate, data_bit, parity, stop):
        self.uart.write(b'\x57\xab\x21'+ struct.pack('<I', baud_rate))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

        self.uart.write(b'\x57\xab\x22'+ struct.pack('<BBB', stop%1, parity%5, data_bit%9))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceTimeout(self, port, timeout):
        self.uart.write(b'\x57\xab\x23'+ struct.pack('<I', timeout))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceNetworkCableDisconnection(self, port, disconnection):
        self.uart.write(b'\x57\xab\x24'+ struct.pack('<B', disconnection%2))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDeviceReceivingPacketLength(self, port, packet_length):
        self.uart.write(b'\x57\xab\x25'+ struct.pack('<I', packet_length))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDestinationIpAddress(self, port, ip):
        self.uart.write(b'\x57\xab\x15'+ bytes(map(int, ip.split('.'))))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setDestinationPortNumber(self, port, port_number):
        self.uart.write(b'\x57\xab\x16'+ struct.pack('<H', port_number))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def setClose(self, port, disconnect):
        self.uart.write(b'\x57\xab\x24'+ struct.pack('<B', disconnect))
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                assert fd.read(1) == struct.pack('<B', 0xaa)

    def getDeviceMode(self):
        self.uart.write(b'\x57\xab\x60')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return fd.read()
        raise Exception

    def getDeviceIpAddress(self):
        self.uart.write(b'\x57\xab\x61')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                ip = struct.unpack('<BBBB', fd.read())
                return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])
        raise Exception

    def getDeviceMaskSubnet(self):
        self.uart.write(b'\x57\xab\x62')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                ip = struct.unpack('<BBBB', fd.read())
                return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])
        raise Exception

    def getDeviceGateway(self):
        self.uart.write(b'\x57\xab\x63')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                ip = struct.unpack('<BBBB', fd.read())
                return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])
        raise Exception

    def getDevicePort(self):
        self.uart.write(b'\x57\xab\x64')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return struct.unpack('<H', fd.read())[0]
        raise Exception

    def getDestinationIpAddress(self):
        self.uart.write(b'\x57\xab\x65')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                ip = struct.unpack('<BBBB', fd.read())
                return '{:03}.{:03}.{:03}.{:03}'.format(ip[0], ip[1], ip[2], ip[3])
        raise Exception

    def getDestinationTimeout(self):
        self.uart.write(b'\x57\xab\x73')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return self.fd.read()
        raise Exception

    def getDestinationPort(self):
        self.uart.write(b'\x57\xab\x66')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                return struct.unpack('<H', fd.read())
        raise Exception

    def getDeviceMacAddress(self):
        self.uart.write(b'\x57\xab\x81')
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
                mac = struct.unpack('<BBBBBB', fd.read())
                return '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])
        raise Exception

if __name__ == "__main__":
    import machine
    uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))
    uart.init(baudrate=9600, bits=8, parity=None, stop=1)
    CFG = machine.Pin(14, machine.Pin.OUT)
    CFG.value(1)
    RST = machine.Pin(17, machine.Pin.OUT)
    RST.value(1)
    
    eth = Pico_eth_ch9121(uart, CFG, RST)
    eth.config()

    CFG.value(0)
    time.sleep(0.1)
    print(eth.getDeviceMode())
    print(eth.getDeviceIpAddress())
    print(eth.getDeviceMaskSubnet())
    print(eth.getDeviceGateway())
    print(eth.getDevicePort())
    CFG.value(1)

    eth.connect(1, '162.159.200.123', 123)

    CFG.value(0)
    time.sleep(0.1)
    eth.getConnectionStatus(0)
    print(eth.getDeviceMacAddress())
    CFG.value(1)
