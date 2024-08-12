import master.socket.WLanPico
import master.socket.SocketUdp

class ArtNet:

    def __init__(self, sock, protocol, portPhysique, univers):
        _sock = sock
        trameDmx = bytearray(530)
        trameDmx[0] = 'A'
        trameDmx[1] = 'r'
        trameDmx[2] = 't'
        trameDmx[3] = '-'
        trameDmx[4] = 'N'
        trameDmx[5] = 'e'
        trameDmx[6] = 't'
        trameDmx[7] = 0
        trameDmx[8] = (protocol & 0xFF00) >> 8
        trameDmx[9] = (protocol & 0x00FF)
        trameDmx[10] = 0
        trameDmx[11] = 0x0E
        trameDmx[12] = 0
        trameDmx[13] = portPhysique & 0xFF
        trameDmx[14] = (univers & 0xFF00) >> 8
        trameDmx[15] = (univers & 0x00FF)
        trameDmx[16] = 0x02
        trameDmx[17] = 0x00

    def setValue(self, canal, valeur):
        trameDmx[18+canal] = valeur;

    def write(self, numeroTrame):
        trameDmx[12] = numeroTrame & 0xFF
        _sock.write(trameDmx)

if __name__ == '__main__':
    try:

        wlan = WLanPico()
        wlan.connect()

        sock = SocketUdp()
        sock.connect("192.168.10.12", 0x1936)

        dmx = ArtNet(sock, 0, 0, 0)
        time.sleep(1)

        dmx.setValue(0, 255)
        dmx.setValue(1, 255)
        dmx.write(0)

        time.sleep(0.1)
    except KeyboardInterrupt:
        sys.exit()

    finally:
        sock.close()
        wlan.disconnect()

