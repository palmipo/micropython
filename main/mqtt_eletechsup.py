from master.net.wlanpico import WLanPico
from master.net.sockettcp import SocketTcp
from master.uart.uartpico import UartPico
from device.modbus.r4dcb08 import R4DCB08
from device.modbus.n4dog16 import N4DOG16
from device.modbus.n4dih32 import N4DIH32
from device.modbus.modbusrtu import ModbusRtu
from device.modbus.modbusexception import ModbusException
from device.pia.ornowe521 import OrnoWe521
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile

import time, binascii, os, sys, machine

R4DCB08_ADR = 0
N4DOG16_ADR = 1
N4DIH32_ADR = 2
R4DCB08_LENGTH = 1
N4DOG16_LENGTH = 16
N4DIH32_LENGTH = 2
TIMEOUT = 2

def publier(sock, texte, valeur):
    pub = MqttPublish(texte, "{}".format(valeur))
    sock.send(pub.buffer)

def recevoir(sock):
    msg = MqttResponse()
    recvBuffer = sock.recv(2)
    type_packet, taille = msg.analayseHeader(recvBuffer)
    recvBuffer = sock.recv(taille)
    return msg.analayseBody(type_packet, taille, recvBuffer)

def main():
    uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
    uart2 = UartPico(bus=1, bdrate=9600, pinTx=4, pinRx=5)
    bus1 = ModbusRtu(uart1)
    bus2 = ModbusRtu(uart2)

    cpt = []
    cpt.append(R4DCB08(0x01, bus2))
    cpt.append(N4DOG16(0x02, bus2))
    cpt.append(N4DIH32(0x04, bus2))

    inp = []
    inp.append(OrnoWe521(14))
    inp.append(OrnoWe521(15))

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

        sock = SocketTcp(timeout=TIMEOUT)
        try:
            sock.connect(SERVER, PORT)

            try:
                rep = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1)
                sock.send(rep.buffer)
                recevoir(sock)

                try:
                    for i in range(N4DOG16_LENGTH):
                        rep = MqttSubcribe(1+i, "command/output/cabane/{}".format(i), 0)
                        sock.send(rep.buffer)
                        recevoir(sock)

                    cpt_seconde = 0
                    fin = False
                    while fin == False:
                        if cpt_seconde == 0:
                            for i in range(R4DCB08_LENGTH):
                                try:
                                    publier(sock, 'status/temperature/cabane/{}'.format(i), cpt[R4DCB08_ADR].read(i))

                                except ModbusException as err:
                                    print('ModbusException', err)

                            for i in range(len(inp)):
                                try:
                                    publier(sock, 'status/energie/cabane/{}'.format(i), inp[i].compteur())

                                except ModbusException as err:
                                    print('ModbusException', err)


                        for i in range(N4DOG16_LENGTH):
                            try:
                                publier(sock, 'status/output/cabane/{}'.format(i), cpt[N4DOG16_ADR].read(i))

                            except ModbusException as err:
                                print('ModbusException', err)

                        for i in range(N4DIH32_LENGTH):
                            try:
                                publier(sock, 'status/input/cabane/{}'.format(i), cpt[N4DIH32_ADR].read(i))

                            except ModbusException as err:
                                print('ModbusException', err)

                        try:
                            rep = recevoir(sock)
                            if type(rep) == MqttPubRecv:
                                for i in range(N4DOG16_LENGTH):
                                    if rep.topic_name == b'command/output/cabane/{}'.format(i):
                                        if rep.text == b'0':
                                            cpt[N4DOG16_ADR].close(i)

                                        elif rep.text == b'1':
                                            cpt[N4DOG16_ADR].open(i)

                        except ModbusException as err:
                            print('ModbusException', err)

                        except OSError as err:
                            print(err)

                        cpt_seconde = (cpt_seconde + 1) % 60
                        
                finally:
                    for i in range(N4DOG16_LENGTH):
                        rep = MqttUnsubcribe(1+i)
                        sock.send(rep.buffer)

            finally:
                print('MqttDisconnect')
                rep = MqttDisconnect()
                sock.send(rep.buffer)

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
