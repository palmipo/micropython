from master.uart.uartpico import UartPico
from master.pia.piapico import PiaOutputPico
import time

class WaveshareTcpServer(WaveshareEthernetCh9121):
    def __init__(self, bus, pinCFG, pinReset):
        super().__init__(bus, pinCFG, pinReset)
        super().setMode(0)

class WaveshareTcpClient(WaveshareEthernetCh9121):
    def __init__(self, bus, pinCFG, pinReset):
        super().__init__(bus, pinCFG, pinReset)
        super().setMode(1)

class WaveshareUdpServer(WaveshareEthernetCh9121):
    def __init__(self, bus, pinCFG, pinReset):
        super().__init__(bus, pinCFG, pinReset)
        super().setMode(2)

class WaveshareUdpClient(WaveshareEthernetCh9121):
    def __init__(self, bus, pinCFG, pinReset):
        super().__init__(bus, pinCFG, pinReset)
        super().config(3)

class WaveshareEthernetCh9121:
    def __init__(self, bus, pinCFG, pinReset):
        self.uart = bus
        self.pinCFG = pinCFG #Pin(pinCFG, Pin.OUT, Pin.PULL_UP)
        self.pinRST = pinReset #Pin(pinReset, Pin.OUT, Pin.PULL_UP)
        self.pinCFG.value(1)
        self.pinRST.value(1)

    def setMode(self, mode):
        self.sendCmd(b'\x57\xab\x10'+mode.to_bytes(1, 'little'))

    def setLocalIp(self, ip):
        self.sendCmd(b'\x57\xab\x11'+bytes(bytearray(ip)))

    def setSubnetMask(self, mask):
        self.sendCmd(b'\x57\xab\x12'+bytes(bytearray(mask)))

    def setGateway(self, gateway):
        self.sendCmd(b'\x57\xab\x13'+bytes(bytearray(gateway)))

    def setLocalPort(self, port):
        self.sendCmd(b'\x57\xab\x14'+port.to_bytes(2, 'little'))

    def setTargetIp(self, ip):
        self.sendCmd(b'\x57\xab\x15'+bytes(bytearray(ip)))

    def setTargetPort(self, port):
        self.sendCmd(b'\x57\xab\x16'+port.to_bytes(2, 'little'))

    def baudRate(self, bd):
        self.sendCmd(b'\x57\xab\x21'+bd.to_bytes(4, 'little'))

    def saveParameters(self):
        self.sendCmd(b'\x57\xab\x0D')

    def execParametersReboot(self):
        self.sendCmd(b'\x57\xab\x0E')

    def leaveConfiguration(self):
        self.sendCmd(b'\x57\xab\x5E')

    def sendCmd(self, cmd):
        self.pinCFG.value(0)
        time.sleep_ms(100)
        self.uart.write(cmd)
        time.sleep_ms(100)
        self.pinCFG.value(1)
        time.sleep_ms(100)

GATEWAY = (192, 168, 10, 254)   # GATEWAY
TARGET_IP = (192, 168, 10, 17)# TARGET_IP
LOCAL_IP = (192,168,10,70)    # LOCAL_IP
SUBNET_MASK = (255,255,255,0) # SUBNET_MASK
LOCAL_PORT1 = 5000             # LOCAL_PORT1
LOCAL_PORT2 = 4000             # LOCAL_PORT2
TARGET_PORT = 3000            # TARGET_PORT
BAUD_RATE = 115200            # BAUD_RATE
eth = WaveshareTcpClient(UartPico(), PiaOutputPico(14), PiaOutputPico(17))
eth.setLocalIp(LOCAL_IP)
eth.setLocalPort(LOCAL_PORT1)
eth.setTargetIp(TARGET_IP)
eth.setTargetPort(TARGET_PORT)
eth.setGateway(GATEWAY)