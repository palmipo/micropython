import time, binascii, ntptime
from waveshare.waveshare_nixie_clock.nixieclock import NixieClock
from waveshare.waveshare_nixie_clock.nixiebipapp import NixieBipApp
from waveshare.waveshare_nixie_clock.nixieconfigapp import NixieConfigApp
from waveshare.waveshare_nixie_clock.nixieledapp import NixieLedApp
from waveshare.waveshare_nixie_clock.nixiemainapp import NixieMainApp
from master.net.wlanpico import WLanPico
from master.net.sockettcp import SocketTcp
from device.net.ntp import Ntp
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile

def recevoir(fd):
    msg = MqttResponse()

    recvBuffer1 = fd.recv(2)
    type_packet, taille = msg.analayseHeader(recvBuffer1)

    recvBuffer2 = fd.recv(taille)
    return msg.analayseBody(type_packet, taille, recvBuffer2)

horloge = NixieClock()
try:
    wifi = ConfigFile("wifi.json")

    wlan = WLanPico()
    wlan.connect(wifi.config()['wifi']['ssid'], wifi.config()['wifi']['passwd'])

#     ntptime.settime()

    bipApp = NixieBipApp(horloge)
    configApp = NixieConfigApp(horloge, wlan)
    ledApp = NixieLedApp(horloge)

    mainApp = NixieMainApp([bipApp, configApp, ledApp])
    mainApp.init()

    cfg = ConfigFile("mqtt.json")
    PORT =  cfg.config()['mqtt']['broker']['port']
    SERVER = cfg.config()['mqtt']['broker']['ip']
    USER = cfg.config()['mqtt']['broker']['user']
    PASSWD = cfg.config()['mqtt']['broker']['passwd']
    CLIENT_ID = binascii.hexlify(machine.unique_id())

    sock = SocketTcp()
    try:
        sock.connect(SERVER, PORT)

        try:
            cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1)
            sock.send(cnx.buffer)
            recevoir(sock)
            
            try:
                sub = MqttSubcribe(1, "capteur/energie/0/activePower", 0)
                sock.send(sub.buffer)
                recevoir(sock)

                sub = MqttSubcribe(2, "capteur/temperature/garage", 0)
                sock.send(sub.buffer)
                recevoir(sock)

                fin = False
                while fin == False:
                    if horloge.kr.isActivated() == True:
                        mainApp.krActivated()

                    if horloge.kl.isActivated() == True:
                        mainApp.klActivated()

                    if horloge.km.isActivated() == True:
                        mainApp.kmActivated()

                    if horloge.ds1321.isActivated() == True:
                        mainApp.rtcActivated()

                    try:
                        pubRecv = recevoir(sock)
                        pubRecv.topic_name, pubRecv.text
                        mainApp.publisherRecev(pubRecv.topic_name, pubRecv.text)
                    except OSError:
                        pass

            finally:
                unsub = MqttUnsubcribe(2)
                sock.send(unsub.buffer)

                unsub = MqttUnsubcribe(1)
                sock.send(unsub.buffer)

        finally:
            discnx = MqttDisconnect()
            sock.send(discnx.buffer)

    finally:    
        sock.disconnect()

finally:    
    wlan.disconnect()
