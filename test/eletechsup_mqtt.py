from master.net.wlanpico import WLanPico
from master.net.sockettcp import SocketTcp
from master.net.pollstream import PollStream
from master.uart.uartpico import UartPico
from device.modbus.r4dcb08 import R4DCB08
from device.modbus.n4dog16 import N4DOG16
from device.modbus.n4dih32 import N4DIH32
from device.modbus.modbusrtu import ModbusRtu
from device.modbus.modbusexception import ModbusException

from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile

import time, binascii, os, sys, machine

TIMEOUT = 300000

def publier(sock, texte, valeur):
    pub = MqttPublish(texte, "{}".format(valeur))
    sock.send(pub.buffer)

def recevoir(sock):
        msg = MqttResponse()

        recvBuffer = sock.recv(2)
        type_packet, taille = msg.analayseHeader(recvBuffer)

        recvBuffer = sock.recv(taille)
        rep = msg.analayseBody(type_packet, taille, recvBuffer)
        if type(rep) == MqttPubRecv:
            print('========> ', rep.topic_name, rep.text, ' <========')
        return rep

def main():
        uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
        uart2 = UartPico(bus=1, bdrate=9600, pinTx=4, pinRx=5)
        bus1 = ModbusRtu(uart1)
        bus2 = ModbusRtu(uart2)

        cpt = []
        cpt.append(R4DCB08(0x01, bus1))
        cpt.append(R4DCB08(0x01, bus2))
        cpt.append(N4DOG16(0x02, bus2))
        cpt.append(N4DIH32(0x04, bus2))

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

#             eletechsup = ConfigFile("eletechsup.json")

            sock = SocketTcp(timeout=30)
            try:
                sock.connect(SERVER, PORT)

                try:

                    cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
                    sock.send(cnx.buffer)
                    recevoir(sock)

                    sub = MqttSubcribe(1, "output/lampe/cabane/0", 0)
                    sock.send(sub.buffer)
                    recevoir(sock)

                    fin = False
                    while fin == False:
                        try:
                            publier(sock, 'capteur/temperature/0', cpt[0].read(0))
                        
                        except ModbusException as err:
                            print('ModbusException', err)

                        try:
                            publier(sock, 'capteur/temperature/9', cpt[1].read(0))
                        
                        except ModbusException as err:
                            print('ModbusException', err)

                        try:
                            publier(sock, 'capteur/bp/all', cpt[3].readAll())
                            publier(sock, 'capteur/bp/1', cpt[3].read(1))
                        
                        except ModbusException as err:
                            print('ModbusException', err)

                        try:
                            rep = recevoir(sock)
                            if rep.topic_name == b'output/lampe/cabane/0':
                                cpt[2].momentary(0)
                        except OSError as err:
                            print('OSError', err)
                        except ModbusException as err:
                            print('ModbusException', err)

                    print('FIN.')
                        
                except ModbusException as err:
                    print('ModbusException', err)
                    fin = True

                finally:
                    print('MqttDisconnect')
                    discnx = MqttDisconnect()
                    sock.send(discnx.buffer)

            finally:
                print('sock.close')
                sock.disconnect()

        finally:
            print('wlan.disconnect')
            wlan.disconnect()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exit")
        sys.quit()

