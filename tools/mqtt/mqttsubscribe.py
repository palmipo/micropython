import network, time, select, binascii, machine, socket, json
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
from master.net.wlanpico import WLanPico

TIMEOUT = 10000

def envoyer(buffer):
    sock.write(buffer)

def recevoir():
    events1 = poule.poll(TIMEOUT)
    for (fd1, event1) in events1:
        if (event1 == select.POLLIN):
            recvBuffer1 = fd1.read(2)

            type_packet, taille = msg.analayseHeader(recvBuffer1)

            events2 = poule.poll(TIMEOUT)
            for (fd2, event2) in events2:
                if (event2 == select.POLLIN):

                    recvBuffer2 = fd2.read(taille)
                    return msg.analayseBody(type_packet, taille, recvBuffer2)

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

    sock = socket.socket()
    try:
        addr = socket.getaddrinfo(SERVER, PORT)[0][-1]
        print(addr)
        sock.connect(addr)
        sock.setblocking(True)

        poule = select.poll()
        poule.register(sock, select.POLLIN | select.POLLERR | select.POLLHUP)

        msg = MqttResponse()
        try:
            cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
            envoyer(cnx.buffer)
            recevoir()
            
            sub = MqttSubcribe(1, "capteur/energie/0/activePower", 0)
            envoyer(sub.buffer)
            recevoir()

            sub = MqttSubcribe(2, "capteur/energie/1/activePower", 0)
            envoyer(sub.buffer)
            recevoir()

            fin = False
            while fin == False:
                try:
                    reponse = recevoir()
                    print(type(reponse))
                    
                except KeyboardInterrupt:
                    fin = True

                except Exception as e:
                    print('exception boucle', type(e), e)

        except Exception as e:
            print(type(e), e)

        finally:
            unsub = MqttUnsubcribe(1)
            envoyer(unsub.buffer)
            recevoir()

            unsub = MqttUnsubcribe(2)
            envoyer(unsub.buffer)
            recevoir()

            discnx = MqttDisconnect()
            envoyer(discnx.buffer)

    finally:    
        sock.close()

finally:    
    wlan.disconnect()
