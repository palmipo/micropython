import struct
from device.modbus.modbusmsg03 import ModbusMsg03
from device.modbus.modbusmsg06 import ModbusMsg06
from device.modbus.modbusrtu import ModbusRtu
from master.uart.uartpico import UartPico
from device.modbus.modbusexception import ModbusException
from tools.mqtt.mqttcodec import *
from tools.configfile import ConfigFile
from master.net.wlanpico import WLanPico
import time, network, select, binascii, machine, socket, json, os, sys

class OR_WE_504:
    def __init__(self, modbus_id, rs485):
        self.modbus_id = modbus_id
        self.bus = rs485

    def voltage(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        v = msg.readHoldingRegisters(0x00, 0x01)
        return v[0]/10

    def intensite(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        a = msg.readHoldingRegisters(0x01, 0x01)
        return a[0]/10

    def frequence(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        f = msg.readHoldingRegisters(0x02, 0x01)
        return f[0]/10

    def activePower(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        ap = msg.readHoldingRegisters(0x03, 0x01)
        return ap[0]

    def reactivePower(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        rp = msg.readHoldingRegisters(0x04, 0x01)
        return rp[0]

    def apparentPower(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        ap = msg.readHoldingRegisters(0x05, 0x01)
        return ap[0]

    def powerFactor(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        pf = msg.readHoldingRegisters(0x06, 0x01)
        return pf[0]/1000

    def activeEnergie(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        ae = msg.readHoldingRegisters(0x07, 0x02)
        return ae[1]

    def reactiveEnergie(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        re = msg.readHoldingRegisters(0x09, 0x02)
        return re[1]

    def setBaudRate(self, baud_rate):
        msg = ModbusMsg06(self.modbus_id, self.bus)
        msg.presetSingleRegister(0x0E, baud_rate)

    def getBaudRate(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        bd = msg.readHoldingRegisters(0x0E, 0x01)
        return bd[0]

    def setModbusId(self, modbus_id):
        msg = ModbusMsg06(self.modbus_id, self.bus)
        msg.presetSingleRegister(0x0F, modbus_id)

    def getModbusId(self):
        msg = ModbusMsg03(self.modbus_id, self.bus)
        bd = msg.readHoldingRegisters(0x0F, 0x01)
        return bd[0]

    # setting：01 28 FE 01 00 02 04 00 00 00 00 FB 12 //00 00 00 00 password
    # return：01 28 FE 01 00 01 C0 24
    def login(self, passwd):
        sendBuffer = bytearray(15)
        msg = ModbusMsg(self.modbus_id, 0x28)
        
        msg.encode(sendBuffer)
        struct.pack_into('>HHBHH', sendBuffer, 2, 0xFE01, 0x0002, 0x04, 0x0000, 0x0000)
        
        recvBuffer = bus.transfer(sendBuffer, 6)

        msg.decode(recvBuffer)

    # Write password：02 10 00 10 00 02 04 11 11 11 11 64 82 //setting password 11 11 11 11
    # return：02 10 00 10 00 02 40 3E
    def passwordEfficacy(self, passwd):
        msg16 = ModbusMsg16(self.modbus_id, self.bus)
        msg16.presetMultipleRegisters(0x10, passwd)

    # setting : 01 28 FE 01 00 02 04 00 00 00 00 -> 00 00 00 00 password
    # return  : 01 28 FE 01 00 01
    def removePassword(self, passwd):
        sendBuffer = bytearray(15)
        msg = ModbusMsg(self.modbus_id, 0x28)
        
        msg.encode(sendBuffer)
        struct.pack_into('>HHBHH', sendBuffer, 2, 0xFE01, 0x0002, 0x04, passwd)
        
        recvBuffer = bus.transfer(sendBuffer, 6)
        
        msg.decode(recvBuffer)
        addr, value = struct.unpack_from('>HH', recvBuffer, 2)

        if addr != 0xFE01:
            raise ModbusException()

        if value != 0x0001:
            raise ModbusException()

TIMEOUT = 1000

def publier(sock, poule, num, texte, valeur):
    pub = MqttPublish("capteur/energie/{}/{}".format(num, texte), "{}".format(valeur))
    sock.write(pub.buffer)

    events = poule.poll(TIMEOUT)

    for (fd, event) in events:
        if (event == select.POLLIN):
    
            recvBuffer = fd.read(2)

            type_packet, taille = msg.analayseHeader(recvBuffer)

            events = poule.poll(TIMEOUT)
            for (fd, event) in events:
                if (event == select.POLLIN):

                    recvBuffer = fd.read(taille)

                    reponse = msg.analayseBody(type_packet, recvBuffer)


def main():
    try:
        uart1 = UartPico(bus=0, bdrate=9600, pinTx=0, pinRx=1)
        uart2 = UartPico(bus=1, bdrate=9600, pinTx=4, pinRx=5)
        bus1 = ModbusRtu(uart1)
        bus2 = ModbusRtu(uart2)

        cpt = []
        cpt.append(OR_WE_504(0x00, bus1))
        cpt.append(OR_WE_504(0x01, bus2))

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
                sock.connect(addr)
                sock.setblocking(True)

                poule = select.poll()
                poule.register(sock, select.POLLIN | select.POLLERR | select.POLLHUP)

                msg = MqttResponse()
                try:

                    cnx = MqttConnect(client_id=CLIENT_ID, user=USER, passwd=PASSWD, retain=0, QoS=0, clean=1, keep_alive=2*TIMEOUT)
                    sock.write(cnx.buffer)

                    events = poule.poll(TIMEOUT)
                    for (fd, event) in events:
                        if (event == select.POLLIN):

                            recvBuffer = fd.read(2)
                            type_packet, taille = msg.analayseHeader(recvBuffer)

                            events = poule.poll(TIMEOUT)
                            for (fd, event) in events:
                                if (event == select.POLLIN):

                                    recvBuffer = fd.read(taille)
                                    reponse = msg.analayseBody(type_packet, recvBuffer)

                            i = 0
                            while True:
                                try:
                                    publier(sock, poule, i, 'voltage', cpt[i].voltage())
                                    publier(sock, poule, i, 'intensite', cpt[i].intensite())
                                    publier(sock, poule, i, 'frequence', cpt[i].frequence())
                                    publier(sock, poule, i, 'activePower', cpt[i].activePower())
                                    publier(sock, poule, i, 'reactivePower', cpt[i].reactivePower())
                                    publier(sock, poule, i, 'apparentPower', cpt[i].apparentPower())
                                    publier(sock, poule, i, 'powerFactor', cpt[i].powerFactor())
                                    publier(sock, poule, i, 'activeEnergie', cpt[i].activeEnergie())
                                    publier(sock, poule, i, 'reactiveEnergie', cpt[i].reactiveEnergie())
                                
                                except ModbusException:
                                    print('ModbusException')

                                except Exception:
                                    print('exception')

                                i = (i + 1) % len(cpt)
                                
                                time.sleep(30)
                    print('FIN.')

                finally:
                    print('MqttDisconnect')
                    discnx = MqttDisconnect()
                    sock.write(discnx.buffer)

            finally:
                print('sock.close')
                sock.close()

        finally:
            print('wlan.disconnect')
            wlan.disconnect()

    except KeyboardInterrupt:
        print("exit")
        sys.exit()

if __name__ == "__main__":
    main()