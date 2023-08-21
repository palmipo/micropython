#import network
import time
#import ubinascii
import socket

#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#wlan.connect('batrahome', 'grenouillette-27')
#while not wlan.isconnected() and wlan.status() >= 0:
#  print("Waiting to connect:")
#  time.sleep(1)
#time.sleep(5)
#print(wlan.ifconfig())

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(socket.getaddrinfo("192.168.10.12", 0x1936)[0][-1])
time.sleep(1)
dmx = bytearray(530)
dmx[0] = 0x41
dmx[1] = 0x72
dmx[2] = 0x74
dmx[3] = 0x2D
dmx[4] = 0x4E
dmx[5] = 0x65
dmx[6] = 0x74
dmx[7] = 0
dmx[8] = 0		# OpCodeLo
dmx[9] = 0x50	# OpCodeHi
dmx[10] = 0x00	# ProtVerHi
dmx[11] = 0x0E	# ProtVerLo
dmx[12] = 0x00	# Sequence
dmx[13] = 0		# Physical
dmx[14] = 0		# SubUni
dmx[15] = 0		# Net
dmx[16] = 0x02	# LengthHi
dmx[17] = 0x00	# Length

#for i in range(255):
i=128
dmx[18] = i
# dmx[19] = 0x00
# dmx[20] = 0x00
# dmx[21] = 0x00
# dmx[22] = 0x00
dmx[23] = 0xFF - i
# dmx[24] = 0x00
# dmx[25] = 0x00
sock.send(dmx)
time.sleep(0.1)
sock.close()

#wlan.disconnect()
