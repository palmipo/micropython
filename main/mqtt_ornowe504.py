from master.net.wlanpico import WLanPico
from master.net.sockettcp import SocketTcp
from master.uart.uartpico import UartPico
from master.pia.piapico import PiaOutputPico, PiaInputPico
from device.modbus.r4dcb08 import R4DCB08
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
    return msg.analayseBody(type_packet, taille, recvBuffer)

def main():
    uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
    uart2 = UartPico(bus=1, bdrate=9600, pinTx=4, pinRx=5)
    bus1 = ModbusRtu(uart1)
    bus2 = ModbusRtu(uart2)

    tempe = R4DCB08(0x01, bus2)
    
    global cpt
    cpt = []
    cpt.append(OR_WE_504(0x01, bus1))
    cpt.append(OR_WE_504(0x02, bus1))
    cpt.append(OR_WE_504(0x03, bus1))
    cpt.append(OR_WE_504(0x04, bus1))

    global out
    out = []
    out.append(PiaOutputPico(6))
    out.append(PiaOutputPico(7))
    out.append(PiaOutputPico(8))
    out.append(PiaOutputPico(9))
    out.append(PiaOutputPico(10))
    out.append(PiaOutputPico(11))
    out.append(PiaOutputPico(12))
    out.append(PiaOutputPico(13))
    
    inp = []
    inp.append(PiaInputPico(14))
    inp.append(PiaInputPico(15))
    inp.append(PiaInputPico(16))
    inp.append(PiaInputPico(17))
    inp.append(PiaInputPico(18))
    inp.append(PiaInputPico(19))
    inp.append(PiaInputPico(20))
    inp.append(PiaInputPico(21))

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

        sock = SocketTcp(timeout=2)
        try:
            sock.connect(SERVER, PORT)

            try:

                cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
                sock.send(cnx.buffer)
                recevoir(sock)

                try:
                    sub = MqttSubcribe(1, "commande/energie/garage/raz", 0)
                    sock.send(sub.buffer)
                    recevoir(sock)

                    for i in range(len(out)):
                        sub = MqttSubcribe(2+i, "commande/output/garage/{}".format(i), 0)
                        sock.send(sub.buffer)
                        recevoir(sock)

                    cpt_seconde = 0
                    fin = False
                    while fin == False:
                        if cpt_seconde == 0:
                            for i in range(len(cpt)):
                                try:
                                    publier(sock, 'status/energie/garage/{}/voltage'.format(i), cpt[i].voltage())
                                    publier(sock, 'status/energie/garage/{}/intensite'.format(i), cpt[i].intensite())
                                    publier(sock, 'status/energie/garage/{}/frequence'.format(i), cpt[i].frequence())
                                    publier(sock, 'status/energie/garage/{}/activePower'.format(i), cpt[i].activePower())
                                    publier(sock, 'status/energie/garage/{}/reactivePower'.format(i), cpt[i].reactivePower())
                                    publier(sock, 'status/energie/garage/{}/apparentPower'.format(i), cpt[i].apparentPower())
                                    publier(sock, 'status/energie/garage/{}/powerFactor'.format(i), cpt[i].powerFactor())
                                    publier(sock, 'status/energie/garage/{}/activeEnergie'.format(i), cpt[i].activeEnergie())
                                    publier(sock, 'status/energie/garage/{}/reactiveEnergie'.format(i), cpt[i].reactiveEnergie())

                                except ModbusException as err:
                                    print('ModbusException', err)

                            for i in range(8):
                                try:
                                    publier(sock, 'status/temperature/garage/{}'.format(i), tempe.read(i))

                                except ModbusException as err:
                                    print('ModbusException', err)

                        for i in range(len(inp)):
                            try:
                                publier(sock, 'status/output/garage/{}'.format(i), inp[i].recv())

                            except ModbusException as err:
                                print('ModbusException', err)

                        try:
                            pubRecv = recevoir(sock)
                            if type(pubRecv) == MqttPubRecv:
                                if pubRecv.topic_name == b'commande/energie/garage/raz':
                                    cpt[int(pubRecv.text)%len(cpt)].clearActiveEnergy(b'\x00\x00\x00\x00')
                                    cpt[int(pubRecv.text)%len(cpt)].clearReactiveEnergie(b'\x00\x00\x00\x00')

                                for i in range(len(out)):
                                    if pubRecv.topic_name == b'commande/output/garage/{}'.format(i):
                                        if int(pubRecv.text) != inp[i].recv():
                                            out[i].send(1)
                                            time.sleep_ms(10)
                                            out[i].send(0)

                        except OSError as err:
                            print(err)

                        except ModbusException as err:
                            print('ModbusException', err)

                        cpt_seconde = (cpt_seconde + 1) % 60
                    
                finally:
                    for i in range(len(out)):
                        sub = MqttUnsubcribe(2+i)
                        sock.send(sub.buffer)

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

