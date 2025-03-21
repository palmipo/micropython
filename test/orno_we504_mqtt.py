from master.uart.uartpico import UartPico
from device.modbus.or_we_504 import OR_WE_504

from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
from master.net.wlanpico import WLanPico
import time, network, select, binascii, machine, socket, json, os, sys

TIMEOUT = 1000

def publier(sock, num, texte, valeur):
    pub = MqttPublish("capteur/energie/{}/{}".format(num, texte), "{}".format(valeur))
    sock.write(pub.buffer)

def recevoir(poule):
    msg = MqttResponse()
    events = poule.poll(TIMEOUT)

    for (fd, event) in events:
        if (event == select.POLLIN):
    
            recvBuffer = fd.read(2)

            type_packet, taille = msg.analayseHeader(recvBuffer)

            events = poule.poll(TIMEOUT)
            for (fd, event) in events:
                if (event == select.POLLIN):

                    recvBuffer = fd.read(taille)

                    reponse = msg.analayseBody(type_packet, taille, recvBuffer)


if __name__ == "__main__":
    try:
        uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
        uart2 = UartPico(bus=1, bdrate=9600, pinTx=4, pinRx=5)
        bus1 = ModbusRtu(uart1)
        bus2 = ModbusRtu(uart2)

        cpt = []
        cpt.append(OR_WE_504(0x01, bus1))
        cpt.append(OR_WE_504(0x01, bus2))

        wlan = WLanPico()
        try:
            wifi = ConfigFile("wifi.json")

            wlan.connect(wifi.config()['wifi']['ssid'], wifi.config()['wifi']['passwd'])

            cfg = ConfigFile("mqtt.json")
            PORT =  cfg.config()['mqtt']['broker']['port']
            SERVER = cfg.config()['mqtt']['broker']['ip']
            USER = cfg.config()['mqtt']['broker']['user']
            PASSWD = cfg.config()['mqtt']['broker']['passwd']
            CLIENT_ID = binascii.hexlify(machine.unique_id())

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                addr = socket.getaddrinfo(SERVER, PORT)[0][-1]
                sock.connect(addr)
                sock.setblocking(True)

                poule = select.poll()
                poule.register(sock, select.POLLIN | select.POLLERR | select.POLLHUP)

                try:

                    cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
                    sock.write(cnx.buffer)
                    recevoir(poule)

                    i = 0
                    while True:
                        try:
                            publier(sock, i, 'voltage', cpt[i].voltage())
                            recevoir(poule)
                            publier(sock, i, 'intensite', cpt[i].intensite())
                            recevoir(poule)
                            publier(sock, i, 'frequence', cpt[i].frequence())
                            recevoir(poule)
                            publier(sock, i, 'activePower', cpt[i].activePower())
                            recevoir(poule)
                            publier(sock, i, 'reactivePower', cpt[i].reactivePower())
                            recevoir(poule)
                            publier(sock, i, 'apparentPower', cpt[i].apparentPower())
                            recevoir(poule)
                            publier(sock, i, 'powerFactor', cpt[i].powerFactor())
                            recevoir(poule)
                            publier(sock, i, 'activeEnergie', cpt[i].activeEnergie())
                            recevoir(poule)
                            publier(sock, i, 'reactiveEnergie', cpt[i].reactiveEnergie())
                            recevoir(poule)
                        
                        except ModbusException:
                            print('ModbusException')

                        except Exception:
                            print('exception')

                        i = (i + 1) % len(cpt)
                        
                        time.sleep(30)
                    print('FIN.')

                finally:
                    print('MqttDisconnect')
                    discnx = MqttDisconnect()
                    sock.write(discnx.buffer)

            finally:
                print('sock.close')
                sock.close()

        finally:
            print('wlan.disconnect')
            wlan.disconnect()

    except KeyboardInterrupt:
        print("exit")
        sys.exit()
