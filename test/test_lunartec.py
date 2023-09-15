from lunartec import Lunartec
from uartpico import UartPico
import network
import time

uart = UartPico(0, 9600, 0, 1)
aff = Lunartec("01", uart)
aff.send("8)")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# addr_mac = wlan.config('mac')
# for b in addr_mac:
#     print(hex(b))
# print(wlan.config('hostname'))

wlan.connect('domoticus', '9foF2sxArWU5')
aff.send("Waiting to connect:")
while not wlan.isconnected() and wlan.status() >= 0:
    time.sleep(1)
time.sleep(5)
aff.send("IP = {:s}:2222".format(wlan.ifconfig()[0]))

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((wlan.ifconfig()[0], 2222))
sock.listen(1)
while True:
    (clientsocket, (ip, port)) = sock.accept()
    r = clientsocket.recv(420).decode()
    while r != 'quit':
        aff.send(r)
        r = clientsocket.recv(420).decode()
    clientsocket.close()
sock.close()
