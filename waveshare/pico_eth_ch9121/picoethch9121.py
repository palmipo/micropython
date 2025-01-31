from waveshare.pico_eth_ch9121.pico_eth_ch9121 import Pico_eth_ch9121
from tools.configfile import ConfigFile
import machine, struct

class PicoEthCh9121:
    def __init__(self, config_file):

        cfg = ConfigFile(config_file)
        
        serial = machine.UART(
            cfg.config()['uart']['0']['bus'],
            baudrate=cfg.config()['uart']['0']['bdrate'],
            tx=machine.Pin(cfg.config()['uart']['0']['pinTx']),
            rx=machine.Pin(cfg.config()['uart']['0']['pinRx']))
        serial.init(
            baudrate=cfg.config()['uart']['0']['bdrate'],
            bits=cfg.config()['uart']['0']['bits'],
            parity=cfg.config()['uart']['0']['parity'],
            stop=cfg.config()['uart']['0']['stop'])
        print(serial)
        CFG = machine.Pin(cfg.config()['pin_cfg'], machine.Pin.OUT)
        CFG.value(1)

        RST = machine.Pin(cfg.config()['pin_reset'], machine.Pin.OUT)
        RST.value(1)

        self.eth = Pico_eth_ch9121(CFG, RST, serial)
        self.eth.config(
            dhcp=cfg.config()['local_addr']['dhcp'],
            ip=cfg.config()['local_addr']['ip'],
            mask=cfg.config()['local_addr']['mask'],
            gateway=cfg.config()['local_addr']['gateway'],
            random_port0=cfg.config()['local_addr']['0']['random_port'],
            port0=cfg.config()['local_addr']['0']['port'])
        print(self.eth)
    def ntp(self):
        self.eth.connect(0, 1, '162.159.200.123', 123)
    
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
        self.eth.uart[0].write(buffer)
    
    def recv(self, length):
        return self.eth[0].uart.read(length)

    def close(self):
        self.eth.setClose(0, 1)

if __name__ == "__main__":
    import time
    eth = PicoEthCh9121('/waveshare/pico_eth_ch9121/pico_eth_ch9121.json')

    eth.eth.CFG.value(0)
    time.sleep(0.1)
    print(eth.eth.getDeviceMode(0))
    print(eth.eth.getDeviceIpAddress())
    print(eth.eth.getDeviceMaskSubnet())
    print(eth.eth.getDeviceGateway())
    print(eth.eth.getDevicePort(0))
    eth.eth.CFG.value(1)

#     eth.eth.connect(1, '162.159.200.123', 123)

    eth.eth.CFG.value(0)
    time.sleep(0.1)
    eth.eth.getConnectionStatus(0)
    mac = (eth.eth.getDeviceMacAddress())
    ip = eth.eth.getDeviceIpAddress()
    eth.eth.CFG.value(1)
    print(ip, mac)

    from master.i2c.i2cpico import I2CPico
    from device.hd44780.lcd2004 import LCD2004
    from device.hd44780.hd44780 import HD44780

    i2c = I2CPico(0, 8, 9)
    lcd_io = LCD2004(0, i2c)
    lcd_io.setBackLight(1)
    lcd = HD44780(lcd_io)
    lcd.clear()
    lcd.home()
    lcd.writeText(mac)
    lcd.setDDRAMAdrress(0x28)
    lcd.writeText(ip)
