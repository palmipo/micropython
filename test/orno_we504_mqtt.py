from master.net.wlanpico import WLanPico
from master.net.sockettcp import SocketTcp
from master.uart.uartpico import UartPico
from device.modbus.or_we_504 import OR_WE_504
from device.modbus.modbusrtu import ModbusRtu
from device.modbus.modbusexception import ModbusException

from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile

import time, binascii, os, sys, machine

TIMEOUT = 1000

def publier(sock, texte, valeur):
    pub = MqttPublish(texte, "{}".format(valeur))
    sock.send(pub.buffer)

def recevoir(fd):
    msg = MqttResponse()

    recvBuffer = fd.recv(2)

    type_packet, taille = msg.analayseHeader(recvBuffer)

    recvBuffer = fd.recv(taille)

    reponse = msg.analayseBody(type_packet, taille, recvBuffer)


def main():
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

            sock = SocketTcp()
            try:
                sock.connect(SERVER, PORT)

                try:

                    cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
                    sock.send(cnx.buffer)
                    recevoir(sock)

                    i = 0
                    fin = False
                    while fin == False:
                        try:
                            publier(sock, 'capteur/energie/{}/voltage'.format(i), cpt[i].voltage())
                            time.sleep(1)

                            publier(sock, 'capteur/energie/{}/intensite'.format(i), cpt[i].intensite())
                            time.sleep(1)

                            publier(sock, 'capteur/energie/{}/frequence'.format(i), cpt[i].frequence())
                            time.sleep(1)

                            publier(sock, 'capteur/energie/{}/activePower'.format(i), cpt[i].activePower())
                            time.sleep(1)

                            publier(sock, 'capteur/energie/{}/reactivePower'.format(i), cpt[i].reactivePower())
                            time.sleep(1)

                            publier(sock, 'capteur/energie/{}/apparentPower'.format(i), cpt[i].apparentPower())
                            time.sleep(1)

                            publier(sock, 'capteur/energie/{}/powerFactor'.format(i), cpt[i].powerFactor())
                            time.sleep(1)

                            publier(sock, 'capteur/energie/{}/activeEnergie'.format(i), cpt[i].activeEnergie())
                            time.sleep(1)

                            publier(sock, 'capteur/energie/{}/reactiveEnergie'.format(i), cpt[i].reactiveEnergie())
                            time.sleep(1)

                        except ModbusException as err:
                            print('ModbusException', err)

                        except Exception as err:
                            print('exception', err)

                        i = (i + 1) % len(cpt)
                        
                        time.sleep(30)
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

