from master.net.wlanpico import WLanPico
from master.net.sockettcp import SocketTcp
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
import time, binascii, os, sys, machine, struct
from machine import Pin
from neopixel import NeoPixel

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
    NB_LED = 8
    pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
    np = NeoPixel(pin, NB_LED)   # create NeoPixel driver on GPIO0 for 8 pixels

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

        sock = SocketTcp(timeout=1)
        try:
            sock.connect(SERVER, PORT)

            try:

                cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1)
                sock.send(cnx.buffer)
                recevoir(sock)

                try:
                    sub = MqttSubcribe(1, "commande/output/ch1/led/0", 0)
                    sock.send(sub.buffer)
                    recevoir(sock)

                    fin = False
                    while fin == False:

                        offset = 0
                        msg = bytearray(NB_LED * 3)
                        for i in range(NB_LED):
                            r, g, b = np[i]
                            struct.pack_into('!BBB', msg, offset, r, g, b)
                            offset += 3
                        print(msg)
                        publier(sock, 'status/output/ch1/led/0', msg)

                        try:
                            pubRecv = recevoir(sock)
                            if type(pubRecv) == MqttPubRecv:
                                if pubRecv.topic_name == b'commande/output/ch1/led/0':
                                    offset = 0
                                    cpt = 0
                                    while offset < len(pubRecv.text) and cpt < NB_LED:
                                        r, g, b = struct.unpack_from('!BBB', pubRecv.text, offset)
                                        print(r,g,b)
                                        offset += 3
                                        np[cpt] = (r, g, b)
                                        cpt += 1
                                    np.write()

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

