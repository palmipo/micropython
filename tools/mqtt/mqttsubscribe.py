import network, time, select, binascii, machine, socket, json
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
from master.net.wlanpico import WLanPico

wlan = WLanPico()
try:
    wifi = ConfigFile("wifi.json")

    wlan.connect(wifi.config()['wifi']['ssid'], wifi.config()['wifi']['passwd'])
    
    TIMEOUT = 1000
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
            print('0')
            cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
            sock.write(cnx.buffer)
            print('0.1')
            events = poule.poll(TIMEOUT)
            for (fd1, event1) in events:
                if (event1 == select.POLLIN):
                    recvBuffer = fd1.read(2)
                    print('0.2')
                    type_packet, taille = msg.analayseHeader(recvBuffer)

                    events = poule.poll(TIMEOUT)
                    for (fd2, event2) in events:
                        if (event2 == select.POLLIN):
                            print('0.3')

                            recvBuffer = fd2.read(taille)
                            reponse2 = msg.analayseBody(type_packet, taille, recvBuffer)
            
                            print('1')
                            sub = MqttSubcribe(1, "capteur/energie/1/activePower", 0)
                            sock.write(sub.buffer)
                            events = poule.poll(TIMEOUT)
                            for (fd3, event3) in events:
                                if (event3 == select.POLLIN):
                                    recvBuffer = fd3.read(2)
                                    type_packet, taille = msg.analayseHeader(recvBuffer)

                                    events = poule.poll(TIMEOUT)
                                    for (fd4, event4) in events:
                                        if (event3 == select.POLLIN):

                                            recvBuffer = fd4.read(taille)
                                            reponse5 = msg.analayseBody(type_packet, taille, recvBuffer)

                                            print('2')
                                            fin = False
                                            while fin == False:
                                                print('3')
                                                events = poule.poll(TIMEOUT)
                                                for (fd5, event5) in events:
                                                    if (event5 == select.POLLIN):
                                                        recvBuffer = fd5.read(2)
                                                        type_packet, taille = msg.analayseHeader(recvBuffer)
                                                        print(type_packet, taille)
                                                        events = poule.poll(TIMEOUT)
                                                        for (fd6, event6) in events:
                                                            if (event6 == select.POLLIN):

                                                                recvBuffer = fd6.read(taille)
                                                                print(recvBuffer)
                                                                reponse4 = msg.analayseBody(type_packet, taille, recvBuffer)
                                                                print(type(reponse4))

        except Exception as e:
            print(type(e), e)

        finally:
            print('4')
            unsub = MqttUnsubcribe(1)
            sock.write(unsub.buffer)
            events = poule.poll(TIMEOUT)
            for (fd, event) in events:
                if (event == select.POLLIN):
                    recvBuffer = fd.read(2)
                    type_packet, taille = msg.analayseHeader(recvBuffer)

                    events = poule.poll(TIMEOUT)
                    for (fd6, event6) in events:
                        if (event6 == select.POLLIN):

                            recvBuffer = fd6.read(taille)
                            reponse4 = msg.analayseBody(type_packet, taille, recvBuffer)

            print('5')
            discnx = MqttDisconnect()
            sock.write(discnx.buffer)

    finally:    
        sock.close()

finally:    
    wlan.disconnect()
