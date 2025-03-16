from device.modbus.modbusexception import ModbusException
import time

class ModbusTcp:
    def __init__(self, address):
        self.sock = socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0)
        addr = socket.getaddrinfo(address, 502)[0][-1]
        self.sock.connect(addr)
        self.sock.setblocking(True)

        self.transactionId = 0
        self.poule = select.poll()
        self.poule.register(sock, select.POLLIN | select.POLLERR | select.POLLHUP)
        self.TIMEOUT = 1000

    def transfer(self, sendBuffer, recvLen):
        buffer = bytearray(len(sendBuffer) + 6)
        
        struct.pack_into(">HHH", buffer, 0, self.transactionId, 0, len(sendBuffer))
        buffer[6:] = sendBuffer
        
        self.rs485.send(buffer)
        
        events = self.poule.poll(self.TIMEOUT)
        for (fd, event) in events:
            if (event == select.POLLIN):
        
                recvBuffer = fd.recv(recvLen)
                if recvBuffer == None:
                    raise ModbusException("buffer de reception vide !")

        return recvBuffer

def main():
    try:
        wlan = WLanPico()
        try:
            wifi = ConfigFile("wifi.json")
            wlan.connect(wifi.config()['wifi']['ssid'], wifi.config()['wifi']['passwd'])
            tcp = ModbusTcp("192.168.1.108")

            try:
                tcp.transfer()

            finally:
                print('sock.close')
                tcp.sock.close()

        finally:
            print('wlan.disconnect')
            wlan.disconnect()

    except KeyboardInterrupt:
        print("exit")
        sys.exit()

if __name__ == "__main__":
    main()
