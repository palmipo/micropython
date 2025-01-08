import network, time, select, binascii, machine, socket
from tools.mqtt.mqttcodec import *

wlan = network.WLAN(network.STA_IF)
try:
    wlan.active(True)
    wlan.connect('domoticus', '9foF2sxArWU5')
    while not wlan.isconnected() and wlan.status() >= 0:
        time.sleep(1)
    time.sleep(5)

    TIMEOUT = 1000
    PORT =  1883
    SERVER = "192.168.1.108"
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

        try:

            cnx = MqttConnect(client_id=CLIENT_ID, user='toff', passwd='crapaud8))', retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
            sock.write(cnx.buffer)
            evnt = poule.poll(TIMEOUT)
            if evnt:
                MqttResponse(evnt[0])

            while True:
                evnt = poule.poll(TIMEOUT)
                if evnt:
                    MqttResponse(evnt[0])

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
