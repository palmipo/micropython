import network, time, select, binascii, machine, socket
from tools.mqtt.mqttcodec import *
from device.spi.st7735 import TFT
from device.spi.sysfont import sysfont
from master.pwm.pwmpico import PwmPico

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

        bl = PwmPico(45)
        bl.setFrequency(1000)
        bl.setDuty(50)
        tft = TFT(spi=machine.SPI(1, baudrate=8000000, sck=machine.Pin(10),mosi=machine.Pin(11),polarity=0, phase=0), aDC=18, aReset=21, aCS=9)
        tft.init_7735(tft.GREENTAB80x160)
        tft.fill(TFT.BLACK)
        tft.text((0, 0), 'subscribe',TFT.WHITE, sysfont, 1)

        try:
            cnx = MqttConnect(client_id=CLIENT_ID, user='toff', passwd='crapaud8))', retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
            sock.write(cnx.buffer)
            evnt = poule.poll(TIMEOUT)
            if evnt:
                MqttResponse(evnt[0])

            sub = MqttSubcribe(1, "a/b", 0)
            sock.write(sub.buffer)
            evnt = poule.poll(TIMEOUT)
            if evnt:
                tft.text((0, 8), 'reception suback ...',TFT.WHITE, sysfont, 1)
                MqttResponse(evnt[0])

            while True:
                evnt = poule.poll(TIMEOUT)
                print(evnt)
                if evnt:
                    tft.text((0, 16), 'reception ...',TFT.WHITE, sysfont, 1)
                    MqttResponse(evnt[0])

        finally:
            unsub = MqttUnsubcribe(1)
            sock.write(unsub.buffer)
            
            discnx = MqttDisconnect()
            sock.write(discnx.buffer)

    finally:    
        sock.close()

finally:    
    wlan.disconnect()
