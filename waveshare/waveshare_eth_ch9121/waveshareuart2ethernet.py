from uartbus import UartPico
import time

class WaveshareUart2Ethernet:
    def __init__(self, bus, pinCFG, pinReset):
        self.uart = bus
        self.pinCFG = Pin(pinCFG, Pin.OUT, Pin.PULL_UP)
        self.pinRST = Pin(pinReset, Pin.OUT, Pin.PULL_UP)
        self.pinCFG.value(1)
        self.pinRST.value(1)

MODE = 1  #0:TCP Server 1:TCP Client 2:UDP Server 3:UDP Client
GATEWAY = (192, 168, 10, 254)   # GATEWAY
TARGET_IP = (192, 168, 10, 17)# TARGET_IP
LOCAL_IP = (192,168,10,70)    # LOCAL_IP
SUBNET_MASK = (255,255,255,0) # SUBNET_MASK
LOCAL_PORT1 = 5000             # LOCAL_PORT1
LOCAL_PORT2 = 4000             # LOCAL_PORT2
TARGET_PORT = 3000            # TARGET_PORT
BAUD_RATE = 115200            # BAUD_RATE

    def config(self):
        self.pinCFG.value(0)
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x10'+MODE.to_bytes(1, 'little'))
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x11'+bytes(bytearray(LOCAL_IP)))
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x12'+bytes(bytearray(SUBNET_MASK)))
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x13'+bytes(bytearray(GATEWAY)))
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x14'+LOCAL_PORT1.to_bytes(2, 'little'))
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x15'+bytes(bytearray(TARGET_IP)))
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x16'+TARGET_PORT.to_bytes(2, 'little'))
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x21'+BAUD_RATE.to_bytes(4, 'little'))
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x0D')
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x0E')
        time.sleep_ms(100)
        self.uart.write(b'\x57\xab\x5E')
        time.sleep_ms(100)
        self.pinCFG.value(1)
        time.sleep_ms(100)
