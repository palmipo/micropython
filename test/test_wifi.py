import network, time, ntptime, ubinascii

wlan = WLanPico()
wlan.connect()

ntptime.settime() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
data_tuple = time.localtime()
laDate = "{} {:02}/{:02}/{:02}".format(data_tuple[6], data_tuple[2], data_tuple[1], data_tuple[0])
lHeure = "{:02}:{:02}:{:02}".format(data_tuple[3], data_tuple[4], data_tuple[5])
print(laDate)
print(lHeure)

# import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind((wlan.ifconfig()[0], 2222))
# sock.listen(1)
# (clientsocket, (ip, port)) = sock.accept()
# buffer = clientsocket.recv(48 * 48).decode()
# print(buffer)
# clientsocket.close()
# sock.close()

wlan.disconnect()
