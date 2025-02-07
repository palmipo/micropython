import serial, select

s = serial.Serial('/dev/ttyAMA0', 115200)
p = select.poll()
p.register(s, select.POLLIN | select.POLLERR | select.POLLHUP)

s.write(b'at+cgps=1,1\r\n')
events = p.poll(60000)
for (fd, event) in events:
    if (event == select.POLLIN):
        print(fd.read())

print('poll')
s.write(b'at+cgpsinfo\r\n')
events = p.poll(60000)
for (fd, event) in events:
  if (event == select.POLLIN):
      print(fd.read())

s.write(b'at+cgps=0\r\n')
events = p.poll(60000)
for (fd, event) in events:
    if (event == select.POLLIN):
        print(fd.read())

s.close()
