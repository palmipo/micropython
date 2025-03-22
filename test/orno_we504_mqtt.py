from master.net.wlanpico import WLanPico
from master.net.sockettcp import SocketTcp
from master.net.pollstream import PollStream
from master.uart.uartpico import UartPico
from device.modbus.or_we_504 import OR_WE_504
from device.modbus.modbusrtu import ModbusRtu
from device.modbus.modbusexception import ModbusException

from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile

#import time, network, select, binascii, machine, socket, json, os, sys
import time, binascii, os, sys, machine

TIMEOUT = 1000

def publier(sock, texte, valeur):
    pub = MqttPublish(texte, "{}".format(valeur))
    sock.write(pub.buffer)

def recevoir(poule):
    fd, event = poule.scrute(TIMEOUT)
    if (event == select.POLLIN):

        #recvBuffer = fd.read(2)
        recvBuffer = fd.recv(2)

        type_packet, taille = msg.analayseHeader(recvBuffer)

        fd, event = poule.poll(TIMEOUT)
        if (event == select.POLLIN):

            #recvBuffer = fd.read(taille)
            recvBuffer = fd.recv(taille)

            msg = MqttResponse()
            reponse = msg.analayseBody(type_packet, taille, recvBuffer)


def main():
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

            mqtt = ConfigFile("mqtt.json")
            PORT =  mqtt.config()['mqtt']['broker']['port']
            SERVER = mqtt.config()['mqtt']['broker']['ip']
            USER = mqtt.config()['mqtt']['broker']['user']
            PASSWD = mqtt.config()['mqtt']['broker']['passwd']
            CLIENT_ID = binascii.hexlify(machine.unique_id())

            orno = ConfigFile("orno.json")

            #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = SocketTcp()
            try:
                #addr = socket.getaddrinfo(SERVER, PORT)[0][-1]
                #sock.connect(addr)
                #sock.setblocking(True)
                sock.connect(SERVER, PORT)

                #poule = select.poll()
                #poule.register(sock, select.POLLIN | select.POLLERR | select.POLLHUP)
                poule = PollStream()
                poule.register(sock.sock)

                try:

                    cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
                    #sock.write(cnx.buffer)
                    sock.send(cnx.buffer)
                    recevoir(poule)

                    i = 0
                    while True:
                        try:
                            publier(sock, 'capteur/energie/{}/voltage'.format(i), cpt[i].voltage())
                            recevoir(poule)
                            publier(sock, 'capteur/energie/{}/intensite'.format(i), cpt[i].intensite())
                            recevoir(poule)
                            publier(sock, 'capteur/energie/{}/frequence'.format(i), cpt[i].frequence())
                            recevoir(poule)
                            publier(sock, 'capteur/energie/{}/activePower'.format(i), cpt[i].activePower())
                            recevoir(poule)
                            publier(sock, 'capteur/energie/{}/reactivePower'.format(i), cpt[i].reactivePower())
                            recevoir(poule)
                            publier(sock, 'capteur/energie/{}/apparentPower'.format(i), cpt[i].apparentPower())
                            recevoir(poule)
                            publier(sock, 'capteur/energie/{}/powerFactor'.format(i), cpt[i].powerFactor())
                            recevoir(poule)
                            publier(sock, 'capteur/energie/{}/activeEnergie'.format(i), cpt[i].activeEnergie())
                            recevoir(poule)
                            publier(sock, 'capteur/energie/{}/reactiveEnergie.format(i)', cpt[i].reactiveEnergie())
                            recevoir(poule)
                        
                        except ModbusException as err:
                            print('ModbusException', err)

                        except Exception as err:
                            print('exception', err)

                        i = (i + 1) % len(cpt)
                        
                        time.sleep(30)
                    print('FIN.')

                finally:
                    print('MqttDisconnect')
                    discnx = MqttDisconnect()
                    #sock.write(discnx.buffer)
                    sock.send(discnx.buffer)

            finally:
                print('sock.close')
                sock.disconnect()

        finally:
            print('wlan.disconnect')
            wlan.disconnect()

    except KeyboardInterrupt:
        print("exit")
        sys.exit()

if __name__ == "__main__":
    main()
