from piapico import PiaPico
from hc1632matrix import Hc1632Matrix

def irq(pin):
    print('appui sur bp {}'.format(pin))

bp_pin = PiaPico(20, irq)
bp_pin = PiaPico(21, irq)
bp_pin = PiaPico(22, irq)

data_pin = PiaPico(8)
write_pin = PiaPico(9)
cs_pin = []
cs_pin.append(PiaPico(14))
cs_pin.append(PiaPico(12))
cs_pin.append(PiaPico(10))
cs_pin.append(PiaPico(15))
cs_pin.append(PiaPico(13))
cs_pin.append(PiaPico(11))
# cs_pin.append(PiaPico(16))
# cs_pin.append(PiaPico(17))
# cs_pin.append(PiaPico(18))
# cs_pin.append(PiaPico(19))

paint = Hc1632Matrix(3, 2, data_pin, write_pin, cs_pin)
paint.fill(0)
paint.show()

import network, time, ntptime, ubinascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('domoticus', '9foF2sxArWU5')
while not wlan.isconnected() and wlan.status() >= 0:
  time.sleep(1)
time.sleep(5)
paint.text(wlan.ifconfig()[0], 0, 0)
paint.show()

ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
data_tuple = time.localtime()
laDate = "{:02}/{:02}/{:02}".format(data_tuple[2], data_tuple[1], data_tuple[0])
lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
paint.text(laDate, 0, 20)
paint.text(lHeure, 0, 30)
paint.show()

# import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind((wlan.ifconfig()[0], 2222))
# sock.listen(1)
# (clientsocket, (ip, port)) = sock.accept()
# buffer = clientsocket.recv(48 * 48).decode()
# clientsocket.close()
# sock.close()

wlan.disconnect()
