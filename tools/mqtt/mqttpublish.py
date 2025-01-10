import network, time, select, binascii, machine, socket, json, os
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
from master.net.wlanpico import WLanPico

wlan = WLanPico()
try:
    cfg = ConfigFile("/config.json")

    wlan.connect(cfg.config()['wifi']['ssid'], cfg.config()['wifi']['passwd'])

    TIMEOUT = 1000
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
            evnt = poule.poll(TIMEOUT)
            if evnt:
                msg.analayse(evnt[0])

            while True:
                evnt = poule.poll(TIMEOUT)
                if evnt:
                    msg.analayse(evnt[0])

                else:
                    pub = MqttPublish("a/b", "coucou")
                    sock.write(pub.buffer)

        finally:
            discnx = MqttDisconnect()
            sock.write(discnx.buffer)

    finally:
        sock.close()

finally:
    wlan.disconnect()
