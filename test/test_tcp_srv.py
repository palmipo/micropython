import network, time, socket, select, ntptime
from master.net.wlanpico import WLanPico

wlan = WLanPico()
try:
    wlan.connect()

    wlan.ntp() # Year, Month、Day, Hour, Minutes, Seconds, DayWeek, DayYear
    # data_tuple = time.localtime()
    # laDate = "{:2}:{:2}:{:2}".format(str(data_tuple[2]), str(data_tuple[1]), str(data_tuple[0]))
    # lHeure = "{:2}:{:2}:{:2}".format(str(data_tuple[3]), str(data_tuple[4]), str(data_tuple[5]))

    sock_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_srv.bind((wlan.ifconfig()[0], 2222))
    sock_srv.listen(1)
    print(sock_srv)

    poll = select.poll()
    poll.register(sock_srv, select.POLLIN | select.POLLHUP | select.POLLERR)
    while True:
        try:
            events = poll.poll(20)
            if not events:
                print('timeout')
            else:
            #     print (events, select.POLLIN, select.POLLOUT, select.POLLHUP, select.POLLERR)
                for (fd, event) in events:
                    if fd == sock_srv:
                        print('sock_srv')
                        if (event == select.POLLIN):
                            (sock_clnt, (ip, port)) = fd.accept()
                            poll.register(sock_clnt, select.POLLIN | select.POLLHUP | select.POLLERR)
                            print('accept')

                    elif:
                        print('sock_clnt')
                        if (event == select.POLLIN):
                            print('recv')

                            r = fd.recv(420).decode()
                            print(len(r))
                            if len(r) == 0:
                                print('close sock_clnt')
                                fd.close()
                                poll.unregister(fd)
        except OSError:
            print('timeout')
    # sock_srv.close()

finally:
    wlan.disconnect()
