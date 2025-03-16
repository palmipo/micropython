import network, time, select, binascii, machine, socket, json, os
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
        sock.setblocking(False)
        # sock.settimeout(20)

        poule = select.poll()
        poule.register(sock, select.POLLIN | select.POLLERR | select.POLLHUP)

        msg = MqttResponse()
        try:

            cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
            sock.write(cnx.buffer)
            events = poule.poll(TIMEOUT)
            for (fd, event) in events:
                if (event == select.POLLIN):
                    # tft.text((0, 16), 'reception ...',TFT.WHITE, sysfont, 1)
                    msg.analayse(fd)

            while True:
                events = poule.poll(TIMEOUT)
                for (fd, event) in events:
                    if (event == select.POLLIN):
                        # tft.text((0, 16), 'reception ...',TFT.WHITE, sysfont, 1)
                        msg.analayse(fd)

                pub = MqttPublish("a/b", "coucou")
                sock.write(pub.buffer)

        finally:
            discnx = MqttDisconnect()
            sock.write(discnx.buffer)

    finally:
        sock.close()

finally:
    wlan.disconnect()
