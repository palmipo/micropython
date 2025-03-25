import network, time, select, binascii, machine, socket, json
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
from master.net.wlanpico import WLanPico

TIMEOUT = 10

def recevoir(fd):
    recvBuffer1 = fd.recv(2)
    type_packet, taille = msg.analayseHeader(recvBuffer1)

    recvBuffer2 = fd.recv(taille)
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

    sock = SocketTcp()
    try:
        sock.connect(SERVER, PORT)

        try:
            cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
            sock.send(cnx.buffer)
            recevoir(sock)
            
            sub = MqttSubcribe(1, "capteur/energie/0/activePower", 0)
            sock.send(sub.buffer)
            recevoir(sock)

            sub = MqttSubcribe(2, "capteur/energie/1/activePower", 0)
            sock.send(sub.buffer)
            recevoir(sock)

            fin = False
            while fin == False:
                try:
                    reponse = recevoir(sock)
                    print(type(reponse))
                    
                except KeyboardInterrupt:
                    fin = True

                except Exception as e:
                    print('exception boucle', type(e), e)

        except Exception as e:
            print(type(e), e)

        finally:
            unsub = MqttUnsubcribe(1)
            sock.send(unsub.buffer)
            recevoir(sock)

            unsub = MqttUnsubcribe(2)
            sock.send(unsub.buffer)
            recevoir(sock)

            discnx = MqttDisconnect()
            sock.send(discnx.buffer)

    finally:    
        sock.close()

finally:    
    wlan.disconnect()
