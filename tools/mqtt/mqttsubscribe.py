import network, time, select, binascii, machine, socket, json
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
from master.net.wlanpico import WLanPico
# from device.spi.st7735 import TFT
# from device.spi.sysfont import sysfont
# from master.pwm.pwmpico import PwmPico

wlan = WLanPico()
try:
    wifi = ConfigFile("/master/net/wifi.json")

    wlan.connect(wifi.config()['wifi']['ssid'], wifi.config()['wifi']['passwd'])
    
    TIMEOUT = 1000
    cfg = ConfigFile("/tools/mqtt/mqtt.json")
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

#         bl = PwmPico(45)
#         bl.setFrequency(1000)
#         bl.setDuty(50)
#         tft = TFT(spi=machine.SPI(1, baudrate=8000000, sck=machine.Pin(10),mosi=machine.Pin(11),polarity=0, phase=0), aDC=18, aReset=21, aCS=9)
#         tft.init_7735(tft.GREENTAB80x160)
#         tft.fill(TFT.BLACK)
#         tft.text((0, 0), 'subscribe',TFT.WHITE, sysfont, 1)

        msg = MqttResponse()
        try:
            print('0')
            cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
            sock.write(cnx.buffer)
            evnt = poule.poll(TIMEOUT)
            if evnt:
                msg.analayse(evnt[0])
            
            print('1')
            sub = MqttSubcribe(1, "a/b", 0)
            sock.write(sub.buffer)
            evnt = poule.poll(TIMEOUT)
            if evnt:
#                 tft.text((0, 8), 'reception suback ...',TFT.WHITE, sysfont, 1)
                msg.analayse(evnt[0])

            print('2')
            fin = False
            while fin == False:
#                 try:
                    print('3')
                    evnt = poule.poll(TIMEOUT)
                    if evnt:
    #                     tft.text((0, 16), 'reception ...',TFT.WHITE, sysfont, 1)
                        msg.analayse(evnt[0])
#                 finally:
#                     fin = True

        finally:
            print('4')
            unsub = MqttUnsubcribe(1)
            sock.write(unsub.buffer)
            evnt = poule.poll(TIMEOUT)
            if evnt:
#                 tft.text((0, 32), 'reception unsuback ...',TFT.WHITE, sysfont, 1)
                msg.analayse(evnt[0])

            print('5')
            discnx = MqttDisconnect()
            sock.write(discnx.buffer)

    finally:    
        sock.close()

finally:    
    wlan.disconnect()
