import network, time, socket, select

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('domoticus', '9foF2sxArWU5')
while not wlan.isconnected() and wlan.status() >= 0:
    time.sleep(1)
time.sleep(5)
print (wlan)

sock_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_srv.bind((wlan.ifconfig()[0], 2222))
sock_srv.listen(1)
print(sock_srv)

poll = select.poll()
poll.register(sock_srv, select.POLLIN)
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
                        (sock_clnt, (ip, port)) = sock_srv.accept()
                        poll.register(sock_clnt, select.POLLIN)
                        print('accept')

                elif fd == sock_clnt:
                    print('sock_clnt')
                    if (event == select.POLLIN):
                        print('recv')

                        r = sock_clnt.recv(420).decode()
                        print(len(r))
                        if len(r) == 0:
                            print('close sock_clnt')
                            sock_clnt.close()
                            poll.unregister(sock_clnt)
    except OSError:
        print('timeout')
# sock_srv.close()

