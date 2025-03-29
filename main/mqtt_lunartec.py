from master.net.wlanpico import WLanPico
from master.net.sockettcp import SocketTcp
from master.uart.uartpico import UartPico
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
from device.lunartec.lunartec import Lunartec

import time, binascii, os, sys, machine, struct
import ntptime

def publier(sock, texte, valeur):
    pub = MqttPublish(texte, "{}".format(valeur))
    sock.send(pub.buffer)

def recevoir(fd):
    msg = MqttResponse()
    recvBuffer = fd.recv(2)
    type_packet, taille = msg.analayseHeader(recvBuffer)
    recvBuffer = fd.recv(taille)
    return msg.analayseBody(type_packet, taille, recvBuffer)


def main():
    uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
    uart2 = UartPico(bus=1, bdrate=9600, pinTx=4, pinRx=5)
    afficheur = Lunartec(1, uart1)
    
    wlan = WLanPico()

    try:
        wifi = ConfigFile("wifi.json")
        wlan.connect(wifi.config()['wifi']['ssid'], wifi.config()['wifi']['passwd'])

        ntptime.settime()
        rtc = machine.RTC()
        afficheur.set_time(rtc.datetime())

        mqtt = ConfigFile("mqtt.json")
        PORT =  mqtt.config()['mqtt']['broker']['port']
        SERVER = mqtt.config()['mqtt']['broker']['ip']
        USER = mqtt.config()['mqtt']['broker']['user']
        PASSWD = mqtt.config()['mqtt']['broker']['passwd']
        CLIENT_ID = binascii.hexlify(machine.unique_id())

        sock = SocketTcp(timeout=10)
        try:
            sock.connect(SERVER, PORT)

            try:
                cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1)
                sock.send(cnx.buffer)
                recevoir(sock)

                try:
                    sub = MqttSubcribe(1, "commande/lunartec", 0)
                    sock.send(sub.buffer)
                    recevoir(sock)

                    fin = False
                    while fin == False:

                        try:
                            pubRecv = recevoir(sock)
                            if type(pubRecv) == MqttPubRecv:
                                if pubRecv.topic_name == b'commande/lunartec':
                                    afficheur.send(pubRecv.text)

                        except OSError as err:
                            print(err)

                    
                finally:
                    unsub = MqttUnsubcribe(1)
                    sock.send(unsub.buffer)

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

