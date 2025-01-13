from waveshare.pico_eth_ch9121.pico_eth_ch9121 import Pico_eth_ch9121
from tools.configfile import ConfigFile
import machine, struct

class PicoEthCh9121:
    def __init__(self, config_file):

        cfg = ConfigFile(config_file)
        
        serial = machine.UART(
            cfg.config()['uart']['bus'],
            baudrate=cfg.config()['uart']['bdrate'],
            tx=machine.Pin(cfg.config()['uart']['pinTx']),
            rx=machine.Pin(cfg.config()['uart']['pinRx']))
        serial.init(
            baudrate=cfg.config()['uart']['bdrate'],
            bits=cfg.config()['uart']['bits'],
            parity=cfg.config()['uart']['parity'],
            stop=cfg.config()['uart']['stop'])

        CFG = machine.Pin(cfg.config()['pin_cfg'], machine.Pin.OUT)
        CFG.value(1)

        RST = machine.Pin(cfg.config()['pin_reset'], machine.Pin.OUT)

        self.eth = Pico_eth_ch9121(serial, CFG, RST)
        self.eth.config(
            dhcp=cfg.config()['local_addr']['dhcp'],
            ip=cfg.config()['local_addr']['ip'],
            mask=cfg.config()['local_addr']['mask'],
            gateway=cfg.config()['local_addr']['gateway'],
            randomport=cfg.config()['local_addr']['randomport'],
            port=cfg.config()['local_addr']['port'])

    def ntp(self):
        self.eth.connect(1, '162.159.200.123', 123)
    
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        try:
            self.send(NTP_QUERY)
            msg = self.recv(48)
        finally:
            self.close()
        val = struct.unpack("!I", msg[40:44])[0]

        # 2024-01-01 00:00:00 converted to an NTP timestamp
        MIN_NTP_TIMESTAMP = 3913056000

        if val < MIN_NTP_TIMESTAMP:
            val += 0x100000000

        # Convert timestamp from NTP format to our internal format

        EPOCH_YEAR = gmtime(0)[0]
        if EPOCH_YEAR == 2000:
            # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
            NTP_DELTA = 3155673600
        elif EPOCH_YEAR == 1970:
            # (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
            NTP_DELTA = 2208988800
        else:
            raise Exception("Unsupported epoch: {}".format(EPOCH_YEAR))

        t = val - NTP_DELTA


        tm = gmtime(t)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

    def send(self, buffer):
        self.eth.uart.write(buffer)
    
    def recv(self, length):
        return self.eth.uart.read(length)

    def close(self):
        self.eth.setClose(0, 1)

if __name__ == "__main__":
    import time
    eth = PicoEthCh9121('/waveshare/pico_eth_ch9121/pico_eth_ch9121.json')

    eth.eth.CFG.value(0)
    time.sleep(0.1)
    print(eth.eth.getDeviceMode())
    print(eth.eth.getDeviceIpAddress())
    print(eth.eth.getDeviceMaskSubnet())
    print(eth.eth.getDeviceGateway())
    print(eth.eth.getDevicePort())
    eth.eth.CFG.value(1)

    eth.eth.connect(1, '162.159.200.123', 123)

    eth.eth.CFG.value(0)
    time.sleep(0.1)
    eth.eth.getConnectionStatus(0)
    print(eth.eth.getDeviceMacAddress())
    eth.eth.CFG.value(1)
